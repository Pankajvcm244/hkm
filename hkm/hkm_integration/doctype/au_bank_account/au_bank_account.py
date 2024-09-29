# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import json
import requests
from frappe.utils import random_string
from hkm.hkm_integration.doctype.au_bank_integration.encryption import encrypt, decrypt
import frappe
from frappe.model.document import Document

PAYOUT_URL = "https://api.aubank.in/CNBPaymentService/paymentCreation"
PAY_ENQUIRY_URL = "https://api.aubank.in/CNBPaymentService/paymentEnquiry"
MINI_STAT_URL = "https://api.aubank.in/CBSAccountMiniStatementService/txn"


class AUBankAccount(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        account_number: DF.Data | None
        bank_account: DF.Link
        corporate_code: DF.Data | None
        corporate_product_name: DF.Data | None
    # end: auto-generated types
    pass

    def fetch_statement(self, from_date, to_date):
        settings = frappe.get_doc("AU Bank Integration")
        payload = {
            "StartDate": from_date,
            "RequestId": random_string(10),
            "OriginatingChannel": "Hari",
            "EndDate": to_date,
            "AccountNumber": self.account_number,
            "ReferenceNumber": "128637162731723742",
            "TransactionBranch": "2011",
        }
        encryption_key = settings.get_password("encryption_key")
        plain_text = json.dumps(payload, separators=(",", ":"))
        print(payload)
        print(encryption_key)
        # print(json.dumps(payload))
        encdata = encrypt(encryption_key, plain_text)
        # encdata = aes_encrypt_data(json.dumps(payload), encryption_key)
        data = {"encvalue": encdata}
        print(data)
        headers = {"Authorization": "Bearer " + settings.get_password("access_token")}
        # headers = {"Authorization": "Bearer upCUpnJz9ksqyBLMw2hkGw3Mq2KP"}
        response = requests.request("POST", MINI_STAT_URL, headers=headers, data=data)
        print(response.text)
        print(response.status_code)

    def payout(self, payment_request):
        settings = frappe.get_doc("AU Bank Integration")
        tx_details = []
        for p in payment_request.items:
            tx_details.append(
                {
                    "paymentMethodName": "NEFT",
                    "remitterAccountNo": self.account_number,
                    "amount": "1.0",  # p.amount,
                    "ifscCode": p.ifsc_code,
                    "payableCurrency": "INR",
                    "beneAccNo": p.bank_account_number,
                    "beneName": p.bank_account_name,
                    "beneCode": "11111",
                    "valueDate": "",
                    "remarks": "HKM-Production",
                    "transactionRefNo": p.name,
                    "paymentInstruction": f"SUPPLIER PAYMENT {p.bank_account_name}",
                    "email": "test@gmail.com",
                    "phoneNo": "999999999",
                }
            )
        payload = {
            "TransactionCreationRequest": {
                "uniqueRequestId": payment_request.name,
                "corporateCode": self.corporate_code,
                "corporateProductCode": self.corporate_product_name,
                "transactionDetails": tx_details,
            }
        }
        ##Dummy

        payload = {
            "TransactionCreationRequest": {
                "uniqueRequestId": "Test0112233M",
                "corporateCode": "21240931",
                "corporateProductCode": "ALLPAYMENTWIMPSBULK",
                "transactionDetails": [
                    {
                        "paymentMethodName": "NEFT",
                        "remitterAccountNo": "1781220613087427",
                        "amount": "1",
                        "ifscCode": "",
                        "payableCurrency": "INR",
                        "beneAccNo": "2302201151638241",
                        "beneCode": "11111",
                        "valueDate": "",
                        "beneName": "APITEST01",
                        "remarks": "H2H API",
                        "transactionRefNo": "APITEST01I",
                        "paymentInstruction": "Payment Instruction 98",
                        "email": "test@gmail.com",
                        "phoneNo": "999999999",
                    }
                ],
            }
        }
        ##Dummy

        encryption_key = settings.get_password("encryption_key")
        encrypted_data = encrypt(
            encryption_key, json.dumps(payload, separators=(",", ":"))
        )
        data = {"encvalue": encrypted_data}
        headers = {"Authorization": "Bearer " + settings.get_password("access_token")}
        response = requests.request("POST", PAYOUT_URL, headers=headers, json=data)
        if response.status_code == 200:
            mesg = decrypt(encryption_key, response.text)
            mesg = json.loads(mesg)
            frappe.errprint(mesg)
            if "responseCode" in mesg and mesg["responseCode"] != "00":
                frappe.msgprint(
                    mesg["responseMessage"],
                    title="Bank Response",
                    indicator="red",
                    raise_exception=1,
                )
            else:
                payment_request.request_id = mesg["TransactionCreationResponse"][
                    "uniqueRequestId"
                ]
                payment_request.batch_number = mesg["TransactionCreationResponse"][
                    "batchNo"
                ]
                payment_request.save()
                frappe.errprint(payload)
                frappe.errprint(mesg)
        else:
            frappe.throw(
                f"Failed with Error <br>Response Code {response.status_code}<br>{response.text}"
            )

    def payment_enquiry(self, payment_request):
        settings = frappe.get_doc("AU Bank Integration")
        encryption_key = settings.get_password("encryption_key")
        payload = {
            "TransactionEnquiryRequest": {
                "uniqueRequestId": payment_request.request_id,
                "transactionRequestId": random_string(10),
                "batchNo": "",
                "transactionRefNo": "",
                "corporateCode": self.corporate_code,
            }
        }

        encrypted_data = encrypt(
            encryption_key, json.dumps(payload, separators=(",", ":"))
        )
        data = {"encvalue": encrypted_data}
        headers = {"Authorization": "Bearer " + settings.get_password("access_token")}
        response = requests.request("POST", PAY_ENQUIRY_URL, headers=headers, json=data)
        if response.status_code == 200:
            mesg = decrypt(encryption_key, response.text)
            frappe.msgprint(mesg, title="Response", indicator="green")
        else:
            frappe.msgprint(
                response.text, title="Error", indicator="red", raise_exception=1
            )


def demo():
    fetch_statement("dfd104a15b")


@frappe.whitelist()
def fetch_statement(au_bank_id):
    au_bank = frappe.get_doc("AU Bank Account", au_bank_id)
    from_date = "01-June-2024"
    to_date = "06-June-2024"
    au_bank.fetch_statement(from_date, to_date)
    # settings = frappe.get_doc("AU Bank Integration")
    # payload = {
    #     "StartDate": "01-June-2024",
    #     "RequestId": "1238713237890",
    #     "OriginatingChannel": "Hari",
    #     "ReferenceNumber": "128637162731723742",
    #     "TransactionBranch": "2011",
    #     "EndDate": "06-July-2024",
    #     "AccountNumber": "1721200110002843",
    # }

    # print(payload)

    # encryption_key = settings.get_password("encryption_key")
    # plain_text = json.dumps(payload, separators=(",", ":"))
    # encrypted_data = encrypt(encryption_key, plain_text)
    # data = {"encvalue": encrypted_data}
    # headers = {"Authorization": f"Bearer {settings.get_password('access_token')}"}
    # response = requests.request(
    #     "POST",
    #     "https://api.aubankuat.in/CBSAccountMiniStatementService/txn",
    #     headers=headers,
    #     json=data,
    # )
    # print(response.text)
    # resp_data = decrypt(encryption_key, response.text)
    # print(resp_data)


def upload_payment():
    """Upload a payment to the AU Bank API."""
    settings = frappe.get_doc("AU Bank Integration")
    url = "https://api.aubankuat.in/CNBPaymentService/paymentCreation"
    encryption_key = settings.get_password("encryption_key")
    payload = {
        "TransactionCreationRequest": {
            "uniqueRequestId": "Test01122369",
            "corporateCode": "29595833",
            "corporateProductCode": "ALLPAYMENTSWOA",
            "transactionDetails": [
                {
                    "paymentMethodName": "RTGS",
                    "remitterAccountNo": "2401201151784662",
                    "amount": "1",
                    "ifscCode": "",
                    "payableCurrency": "INR",
                    "beneAccNo": "2302201151638241",
                    "beneCode": "11111",
                    "valueDate": "",
                    "beneName": "APITEST01",
                    "remarks": "H2H API",
                    "transactionRefNo": "APITEST0C",
                    "paymentInstruction": "Payment Instruction 98",
                    "email": "test@gmail.com",
                    "phoneNo": "999999999",
                }
            ],
        }
    }

    # {
    #     "TransactionCreationRequest": {
    #         "uniqueRequestId": "Test0112252",
    #         "corporateCode": "29595833",
    #         "corporateProductCode": "ALLPAYMENTSWOA",
    #         "transactionDetails": [
    #             {
    #                 "paymentMethodName": "RTGS",
    #                 "remitterAccountNo": "2401201151784662",
    #                 "amount": "10000",
    #                 "ifscCode": "",
    #                 "payableCurrency": "INR",
    #                 "beneAccNo": "2302201151638241",
    #                 "beneCode": "11111",
    #                 "valueDate": "31-Aug-2024",
    #                 "beneName": "APITEST01",
    #                 "remarks": "H2H API",
    #                 "transactionRefNo": "APITEST01",
    #                 "paymentInstruction": "Payment Instruction 98",
    #                 "email": "test@gmail.com",
    #                 "phoneNo": "999999999",
    #             }
    #         ],
    #     }
    # }
    print(payload)
    encrypted_data = encrypt(encryption_key, json.dumps(payload, separators=(",", ":")))
    data = {"encvalue": encrypted_data}
    headers = {"Authorization": "Bearer " + settings.get_password("access_token")}
    response = requests.request("POST", url, headers=headers, json=data)
    print(response.text)
    mesg = decrypt(encryption_key, response.text)
    print(mesg)
    print(response.status_code)
    print(response.text)


# {"TransactionCreationResponse":{"uniqueRequestId":"TestA081","batchNo":"01020924012","responseMessage":"ACCEPTED","responseCode":"00"}}
def payment_enquiry():
    settings = frappe.get_doc("AU Bank Integration")
    url = "https://api.aubankuat.in/CNBPaymentService/paymentEnquiry"
    encryption_key = settings.get_password("encryption_key")
    payload = {
        "TransactionEnquiryRequest": {
            "uniqueRequestId": "UI12123",
            "transactionRequestId": "TestA0822",
            "batchNo": "",
            "transactionRefNo": "",
            "corporateCode": "29595833",
        }
    }

    encrypted_data = encrypt(encryption_key, json.dumps(payload, separators=(",", ":")))
    data = {"encvalue": encrypted_data}
    headers = {"Authorization": "Bearer " + settings.get_password("access_token")}
    response = requests.request("POST", url, headers=headers, json=data)
    # resp = "DUp4iiL8WsUPQ9LVyvtlnCna3qlESndq5prRRRlSmKyXzC41rsF0D9B9oDasqJb2i4h0XLR8HSbrsrfGuAAnZ92v/2MBYlIMftuZtSkIon0DgTM5qvpO0locSVhCJ8q79a4BA5P5/HLg+ANgaz930rks+nI9q9/zkMM9jFIcGvfXF+NUbg1fzA/xMWg11sbvMdW0QTLO586Pt0yK56eYllpY2amXn8cRUl9fvFRds7Rz/XRiphR5WIn9t30qFJBy7q2HjWjsC0G5hfnEhU5KopoUW3ZR7bE4OJ1ld6RPQh94IxYgPkzw+tzRktlnKYwvmRt73QvvxF+2lx5FIqecLvsfY9Lh+do7VB3YGBN0fqMivDk1nfxguAzhOVBZkCPHe+o/l1lzXcWLxkT2cEw56D6Y/XGdIISr4FRuq8G/Vtx/10TtTdQDzkXiHiGv32rp8iZ+J/3AnXtRle/IQerp6dhlBHYdoOC5IYjpQl7TG2WUs0QSYBJ1ie0AyucOpJRX4tyMZADpdmNgFM5COeQZnJpa7njC6ekdueReiAYLXzYHx+FUdkgChvyA2Zm3QJGmK5u+WfyIxItDY4qqgSYmA8MZLV2jj9cbqYZcje0xdPSx21VXT+4TG0BariUkP7ExwFgfE1i1sPhOdk52XlVyzl00YKWTMll95WgQ9MQmxxVC8KTHSE/vdf4CVpgrcX0hFIFKicTk3fJQW02BJ3dhPEzSDzaMWKOdPsC3zuiGck3eFsgVi+hMteyuKtaC9VNCqhbS8Ckegu/UqB1C4HZNcY3WwoLOvbbM2eZqpMA5hESUiJGQOQA672wyWKzOJzyE+b45x6EjxB6r2eiHg3EveEf5boO8y2z6V+vTnM7TtLhSJhjZLnGsitRzJDMQlYpN9v7XgdoyQ/nL4VScQcY2s5sARwdGEhbU21E7JNUpKrcpaVqOPK7s6ZC5L05TYEhhFcywx41cFLGOfdXyKwFt0K2Ar4sxfL6ytNtMo+SFHmp834BOsWVo7ReHdULA2EIfqr6X5vGe/5Q73CugYMJa17Cuo5/K+yJvvLjAGhMHvYlZruImndQ2VTxJKu3oX/XnJ5lFj/h9Z//ULSu75nofJ5uyUJq14JfcXwSTeXnYtnOHO14U3keXLad1lm9tfNr3CHgbXzXrkiXhZ1dbUQgSfdH94tg3apxHmYSH15B745DB1sshgvU4H8/4wKO5X6GmhMcQDOUYVgr19vNYm8kekYoIxZ2uOh8YhDhpo2jO2kTDzUgu1qoaAAPqD0Uv5hIayVVMyphxjaGOtM9zlkqC8vOh1I5eIHmEPZe1hDJvl/TnrMIeEfdXAR3V++PgFZtHJSUdfg7vp4dT/bmcMURTkENl6H+11oVYfHy6k2eQVHmnINGO9QninwSlZplBdG0vyKa3XjeXzdJSAcf+CDRzszlpGdrbV6Pfy9iMNfAkINyaiuSKuXcxYe9V+d3KcCxGH4588ztdOAD6b9DuvTjd7IVp2lnzU0rtn6KdvwUolFFbt2shTbsxn/prj/QgK88UmPogYQkQaW50/BhsveQ4OHnYK5ScDlg02M/BqDdzNLti6/pYa3hwdogkDlbJf0UCMRT7oPZBym8oqTfqCYztnw=="
    print(response.text)
    mesg = decrypt(encryption_key, response.text)
    print(mesg)
