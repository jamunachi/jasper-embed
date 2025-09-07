from frappe import _

def get_data():
    return [
        {
            "label": _("Jasper Embed"),
            "icon": "octicon octicon-file",
            "items": [
                {
                    "type": "doctype",
                    "name": "Jasper Report",
                    "label": _("Jasper Report"),
                },
                {
                    "type": "doctype",
                    "name": "Jasper Server Settings",
                    "label": _("Jasper Server Settings"),
                }
            ]
        }
    ]
