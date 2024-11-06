# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
import requests
import base64
from hkm.hkm_integration.doctype.au_bank_integration.encryption import encrypt
from frappe.model.document import Document

OAUTH_URL = "https://api.aubank.in/oauth/accesstoken?grant_type=client_credentials"


class AUBankIntegration(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        access_token: DF.Password | None
        client_key: DF.Data | None
        client_secret: DF.Password | None
        encryption_key: DF.Password | None
    # end: auto-generated types
    pass

    def generate_token(self):
        credentials = self.client_key + ":" + self.get_password("client_secret")
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
        }
        response = requests.request("GET", OAUTH_URL, headers=headers)
        print(response.text)
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
            self.save()
            frappe.db.commit()

@frappe.whitelist()
def refresh_token():
    frappe.only_for("Accounts Manager")
    settings = frappe.get_doc("AU Bank Integration")
    settings.generate_token()
