import json
import requests
import frappe

def _user_has_access(report_doc) -> bool:
    """Return True if current user has any of the roles listed on the report (or if none listed)."""
    roles = [r.role for r in getattr(report_doc, "roles", [])] or []
    if not roles:
        return True
    user_roles = set(frappe.get_roles(frappe.session.user))
    return bool(user_roles.intersection(roles))

@frappe.whitelist()
def get_reports_for_doctype(doctype: str) -> list:
    """Return enabled Jasper Report mappings for a given doctype, filtered by user roles."""
    names = frappe.get_all(
        "Jasper Report",
        filters={"reference_doctype": doctype, "enabled": 1},
        pluck="name"
    )
    out = []
    for name in names:
        doc = frappe.get_doc("Jasper Report", name)
        if _user_has_access(doc):
            out.append({
                "name": doc.name,
                "report_label": doc.report_label,
                "report_uri": doc.report_uri,
                "report_for": doc.report_for,
                "default_format": doc.default_format
            })
    return out

@frappe.whitelist()
def run(report_name: str, params=None, fmt: str = "pdf"):
    """Execute a mapped report by name; stream result into a private File.
    Applies role visibility and optionally emails the output if configured.
    """
    doc = frappe.get_doc("Jasper Report", report_name)
    if not doc.enabled:
        frappe.throw("Report is disabled.")
    if not _user_has_access(doc):
        frappe.throw("You do not have permission to run this report.")

    settings = frappe.get_single("Jasper Server Settings")
    base_url = (settings.server_url or "").rstrip("/")
    if not base_url:
        frappe.throw("Jasper Server URL is not configured.")

    username = settings.username
    password = settings.get_password("password")

    # Build params
    p = {}
    if params:
        if isinstance(params, str):
            p = json.loads(params)
        else:
            p = params

    # Call JasperReports Server REST v2
    url = f"{base_url}/rest_v2/reports{doc.report_uri}.{fmt}"
    verify = bool(settings.verify_ssl)
    r = requests.get(url, params=p, auth=(username, password), timeout=int(settings.timeout or 120), verify=verify)
    try:
        r.raise_for_status()
    except Exception:
        text = r.text[:1000] if r.text else str(r.status_code)
        frappe.throw(f"Jasper error {r.status_code}: {text}")

    # Save file in ERPNext
    ext = fmt.lower()
    base_fname = doc.report_label or doc.name
    if "docname" in p:
        base_fname += f"-{p['docname']}"
    fname = f"{base_fname}.{ext}"

    filedoc = frappe.get_doc({
        "doctype": "File",
        "file_name": fname,
        "is_private": 1,
        "content": r.content
    }).insert(ignore_permissions=True)

    # Optional auto-email
    if getattr(doc, "email_after_generation", 0):
        recipients = []
        if getattr(doc, "email_to", None):
            recipients = [x.strip() for x in doc.email_to.split(",") if x.strip()]
        if recipients:
            subject = doc.email_subject or (doc.report_label or report_name)
            message = doc.email_body or "Auto-generated report from Jasper Embed."
            try:
                frappe.sendmail(
                    recipients=recipients,
                    subject=subject,
                    message=message,
                    attachments=[{"fname": fname, "fcontent": r.content}]
                )
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Jasper Embed: Email send failed")

    return {"file_url": filedoc.file_url}
