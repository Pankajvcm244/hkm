### This is one place for keeping all fixtures of any other custom apps as well. If we just have other custom apps instead of this, then we have to manually copy-paste it there to begin with initial fixtures.


### This file has to be dynamically changed everytime, we need to send some customisations to other sites.

custom_fixtures = [
    "DJ Receipt Format",
    # "Wiki Space",
    # "Wiki Page",
    # "S3 Backup Settings",
    # "DFP External Storage",
    # # "Sadhana Parameter",
    # "SMS Settings",
    # "DJ Receipt Format",
    "Workflow Action Master",
    "Workflow State",
    "Role",
    {
        "dt": "Workflow",
        "filters": [
            ["is_active", "=", 1],
            [
                "document_type",
                "in",
                [
                    "Donation Receipt",
                    "Purchase Order",
                    "Donor ECS Creation Request",
                ],
            ],
        ],
    },
    {
        "dt": "Custom Field",
        "filters": [
            [
                "dt",
                "in",
                [
                    "Material Request",
                    "Purchase Order",
                    "Purchase Receipt",
                    "Purchase Invoice",
                    "Sales Invoice",
                    "Stock Entry",
                    "Payment Entry",
                    "Journal Entry",
                    "Customer",
                    "Asset" "Supplier",
                ],
            ],
        ],
    },
    {
        "dt": "Property Setter",
        "filters": [
            # [
            #     "doc_type",
            #     "in",
            #     ["Purchase Invoice", "Sales Invoice", "Stock Entry", "Payment Entry"],
            # ],
        ],
    },
    "Custom DocPerm",
    "DJ Mode of Payment",
]
