from uuid import uuid4

from .helpers import etsi_datetime


class LEA:
    def __init__(self, country_code: str, unique_id: str, delivery_url: str):
        self.sender_country_code = country_code
        self.sender_unique_id = unique_id
        self.delivery_url = delivery_url

    def generate_103120_query(
        self, objects_to_create: list, receiver_country_code: str, receiver_unique_id
    ) -> dict:
        return {
            "Header": {
                "@xmlns": "http://uri.etsi.org/03120/common/2019/10/Core",
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "@xmlns:common": "http://uri.etsi.org/03120/common/2016/02/Common",
                "@xmlns:task": "http://uri.etsi.org/03120/common/2020/09/Task",
                "SenderIdentifier": {
                    "CountryCode": self.sender_country_code,
                    "UniqueIdentifier": self.sender_unique_id,
                },
                "ReceiverIdentifier": {
                    "CountryCode": receiver_country_code,
                    "UniqueIdentifier": receiver_unique_id,
                },
                "TransactionIdentifier": str(uuid4()),
                "Timestamp": etsi_datetime(),
                "Version": {
                    "ETSIVersion": "V1.16.1",
                    "NationalProfileOwner": "XX",
                    "NationalProfileVersion": "v1.0",
                },
            },
            "Payload": {
                "RequestPayload": {
                    "ActionRequests": {
                        "ActionRequest": [
                            {"ActionIdentifier": i, "CREATE": {"HI1Object": o}}
                            for i, o in enumerate(objects_to_create)
                        ]
                    }
                }
            },
        }

    def generate_empty_LDTaskRequest(
        self, task_ref: str, request_type: str, delivery_url: str
    ) -> dict:
        return {
            "@xsi:type": "{http://uri.etsi.org/03120/common/2020/09/Task}LDTaskObject",
            "ObjectIdentifier": str(uuid4()),
            "CountryCode": self.sender_country_code,
            "OwnerIdentifier": self.sender_unique_id,
            "task:Reference": task_ref,
            "task:RequestDetails": {
                "task:Type": {
                    "common:Owner": "ETSI",
                    "common:Name": "TS103976RequestType",
                    "common:Value": request_type,
                },
                "task:RequestValues": {"task:RequestValue": []},
            },
            "task:DeliveryDetails" : {
                  "task:DeliveryDestination": [
                    {
                      "task:DeliveryAddress": {
                        "task:URL": delivery_url
                      }
                    }
                  ]
            }
        }

    def generate_vin_to_comms_id(
        self,
        receiver_country_code="XX",
        receiver_unique_id="Receiver",
        task_ref="XX-X-XXX",
        vin="1G9Y817H34LSP7293",
    ):
        ld_task = self.generate_empty_LDTaskRequest(
            task_ref, "VINtoCommsID", self.delivery_url
        )
        ld_task["task:RequestDetails"]["task:RequestValues"][
            "task:RequestValue"
        ].append(
            {
                "task:FormatType": {
                    "task:FormatOwner": "ETSI",
                    "task:FormatName": "VIN",
                },
                "task:Value": vin,
            }
        )
        hi1_request = self.generate_103120_query(
            [ld_task], receiver_country_code, receiver_unique_id
        )
        return hi1_request
