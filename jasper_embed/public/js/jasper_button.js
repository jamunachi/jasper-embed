// Add Jasper buttons on any form that has mappings
frappe.ui.form.on('*', {
  refresh(frm) {
    // Only on saved docs
    if (frm.is_new()) return;

    frappe.call({
      method: 'jasper_embed.jasper_embed.api.get_reports_for_doctype',
      args: { doctype: frm.doctype },
      callback: function(r) {
        const reports = r.message || [];
        if (!reports.length) return;

        const group = __('Print');
        reports.forEach(rep => {
          const label = rep.report_label || rep.name;
          const fmt = rep.default_format || 'pdf';

          frm.add_custom_button(`${label} (${fmt.toUpperCase()})`, () => {
            const params = { docname: frm.doc.name };
            frappe.call({
              method: 'jasper_embed.jasper_embed.api.run',
              args: {
                report_name: rep.name,
                params: params,
                fmt: fmt
              },
              freeze: true,
              callback: function(res) {
                if (res.message && res.message.file_url) {
                  window.open(res.message.file_url, '_blank');
                } else {
                  frappe.msgprint(__('No file returned from Jasper.'));
                }
              }
            });
          }, group);
        });
      }
    });
  }
});
