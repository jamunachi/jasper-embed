# jasper_embed

Embed **JasperReports Server** reports inside **Frappe/ERPNext** with per-Doctype mappings.

## Features
- Define multiple Reports mapped to multiple Doctypes (Form/List)
- Auto-injected buttons on mapped forms
- Run via REST to JasperReports Server and store output as private `File`
- Output formats: PDF / XLSX

## Quick Install
```bash
bench get-app /path/to/jasper_embed
bench --site your.site install-app jasper_embed
```

## v0.2
- **Role-based visibility per mapping**: add rows under *Allowed Roles* to restrict who sees/runs a report. Leave empty to allow all.
- **Auto email after generation**: enable *Auto Email After Generation*, set recipients, subject, and body. The generated file is attached to the email.
