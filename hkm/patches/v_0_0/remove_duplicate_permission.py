import frappe


def execute():
    query = frappe.db.sql(
        """
    SELECT 
        parent,
        role,
        if_owner,
        permlevel, 
        `select`,   
        `read`,
        `write`,
        `create`,
        `delete`,
        `submit`,
        `cancel`,
        `amend`,
        `report`,
        `export`,
        `import`,
        `share`,
        `print`,
        `email`,
        COUNT(*) AS duplicate_count
    FROM `tabCustom DocPerm`
    GROUP BY 
        parent, role, if_owner, permlevel, `select`, `read`, `write`, `create`, `delete`, 
        `submit`, `cancel`, `amend`, `report`, `export`, `import`, `share`, `print`, `email`
    HAVING COUNT(*) > 1
""",
        as_dict=1,
    )
    for row in query:
        duplicate = frappe.get_all(
            "Custom DocPerm",
            filters={
                "parent": row.parent,
                "role": row.role,
                "if_owner": row.if_owner,
                "permlevel": row.permlevel,
                "select": row.select,
                "read": row.read,
                "write": row.write,
                "create": row.create,
                "delete": row.delete,
                "submit": row.submit,
                "cancel": row.cancel,
                "amend": row.amend,
                "report": row.report,
                "export": row.export,
                "share": row.share,
                "print": row.print,
                "email": row.email,
                "import": row["import"],
            },
            pluck="name",
        )
        print(duplicate)
        for idx, i in enumerate(duplicate, 1):
            if idx == 1:
                continue
            frappe.delete_doc("Custom DocPerm", i)

    frappe.db.commit()
