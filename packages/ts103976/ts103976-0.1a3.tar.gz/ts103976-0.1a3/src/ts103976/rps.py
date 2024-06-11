# Implements a simple RPS
import logging

from uuid import uuid4
from datetime import datetime
from copy import deepcopy
from re import compile
import random
from hashlib import sha1
from dataclasses import dataclass
from typing import List
from json import dumps

from requests import post

from .validator import TS103120Validator
from .helpers import etsi_datetime


@dataclass
class FulfilmentOutcome:
    errorCode: int = 0
    errorDescription: str = ""
    updatedObject: dict = None
    records: List = None

class RPS:
    def __init__(
        self,
        ReceiverCC="XX",
        ReceiverID="RPSReceiver",
        AllowAnyReceiverID=False,
        AsyncResponse=True,
    ):
        self.receiverCC = ReceiverCC
        self.receiverID = ReceiverID
        self.allowAnyReceiverID = AllowAnyReceiverID
        self.validator = TS103120Validator()
        self.VIN_regex = compile(r"^[A-HJ-NPR-Z0-9]{17}$")

    def _generate_top_level_error(self, error_message: str) -> dict:
        return {
            "@xmlns": "http://uri.etsi.org/03120/common/2019/10/Core",
            "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "@xmlns:common": "http://uri.etsi.org/03120/common/2016/02/Common",
            "Header": {
                "SenderIdentifier": {
                    "CountryCode": "ZZ",
                    "UniqueIdentifier": "UNKNOWN",
                },
                "ReceiverIdentifier": {
                    "CountryCode": self.receiverCC,
                    "UniqueIdentifier": self.receiverID,
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
                "ResponsePayload": {
                    "ErrorInformation": {
                        "ErrorCode": 3007,
                        "ErrorDescription": error_message,
                    }
                }
            },
        }

    def _copy_header_from_request(self, request: dict) -> dict:
        header = deepcopy(request["Header"])
        header["Timestamp"] = etsi_datetime()
        return header

    def _generate_action_error(
        self, action_id: int, error_code: int, message: str
    ) -> dict:
        return {
            "ActionIdentifier": action_id,
            "ErrorInformation": {"ErrorCode": error_code, "ErrorDescription": message},
        }

    def _generate_create_response(
        self, action_id, object_id, updated_object=None
    ) -> dict:
        result = {
            "ActionIdentifier": action_id,
            "CREATEResponse": {"Identifier": object_id},
        }
        if updated_object is not None:
            result["CREATEResponse"]["HI1Object"] = updated_object
        return result

    def _parse_message(self, request: dict, context: dict = {}) -> dict:
        context["request"] = request
        errors = self.validator.validate(request)
        if len(errors) > 0:
            error_str = ""
            for error in errors:
                error_str += str(error)
            return self._generate_top_level_error(error_str)
        given_receiver_id = request["Header"]["ReceiverIdentifier"]
        if (not self.allowAnyReceiverID) and (
            (given_receiver_id["UniqueIdentifier"] != self.receiverID)
            or (given_receiver_id["CountryCode"] != self.receiverCC)
        ):
            return self._generate_top_level_error(
                f"Incorrect ReceiverID given: {given_receiver_id}"
            )
        response = {
            "Header": self._copy_header_from_request(request),
            "Payload": {"ResponsePayload": {"ActionResponses": {"ActionResponse": []}}},
        }
        action_responses = response["Payload"]["ResponsePayload"]["ActionResponses"][
            "ActionResponse"
        ]
        next_action_id = 0
        for action_request in request["Payload"]["RequestPayload"]["ActionRequests"][
            "ActionRequest"
        ]:
            action_id = action_request["ActionIdentifier"]
            if action_id != next_action_id:
                action_responses.append(
                    self._generate_action_error(
                        3007,
                        action_id,
                        f"Action request {action_id} is out-of-order, expecting {next_action_id}",
                    )
                )
                continue
            action_responses.append(self._parse_action(action_request, context))
        return response

    def _parse_action(self, action: dict, context: dict = {}) -> dict:
        action_identifier = action["ActionIdentifier"]
        action_type = list(action.keys())[1]
        if action_type != "CREATE":
            return self._generate_action_error(
                action_identifier, 3001, f"Action type {action_type} not supported"
            )
        obj = action["CREATE"]["HI1Object"]
        if (
            obj["@xsi:type"]
            != "{http://uri.etsi.org/03120/common/2020/09/Task}LDTaskObject"
        ):
            return self._generate_action_error(
                action_identifier, 3001, f"Object type {obj['@xsi:type']} not supported"
            )
        request_details = obj["task:RequestDetails"]
        delivery_url = obj["task:DeliveryDetails"]["task:DeliveryDestination"][0]["task:DeliveryAddress"]["task:URL"] # TBD - V fragile obvs
        task_reference = obj["task:Reference"] # TBD - error handling
        request_type = request_details["task:Type"]
        if (
            request_type["common:Owner"] != "ETSI"
            or request_type["common:Name"] != "TS103976RequestType"
        ):
            return self._generate_action_error(
                action_identifier,
                3001,
                f"Request type from unknown dictionary {request_type} not supported.",
            )
        query_type = request_type["common:Value"]
        if query_type == "VINtoCommsID":
            result = self._fulfil_VINtoCommsID(action, context)
            if result.errorCode != 0:
                return self._generate_action_error(
                    action_identifier, result.errorCode, result.errorDescription
                )
            else:
                self._deliver_response(result, context['request'], task_reference, delivery_url)
                return self._generate_create_response(
                    action_identifier, obj["ObjectIdentifier"], result.updatedObject
                )
        # elif query_type == "CommsIDtoVINRecord":
        #     return {}}
        # elif query_type == "VINtoLocationRecord":
        #     return {}}
        else:
            return self._generate_action_error(
                action_identifier,
                3007,
                f"Invalid request type {query_type} - see TS 103 976 table 6.2.5-1 for valid values",
            )

    def _complete_LDRequest(self, ld_request_object: dict) -> dict:
        ld_request_object["LDTaskStatus"] = {
            "common:Owner": "ETSI",
            "common:Name": "LDTaskStatus",
            "common:Value": "Disclosed",
        }
        return ld_request_object

    def _fulfil_VINtoCommsID(
        self, action: dict, context: dict = {}
    ) -> FulfilmentOutcome:
        # TBD - fail if you specify a start or end time
        obj = action["CREATE"]["HI1Object"]
        request_details = obj["task:RequestDetails"]
        request_values = request_details["task:RequestValues"]["task:RequestValue"]
        if len(request_values) != 1:
            return FulfilmentOutcome(
                3007,
                f"Unexpected number of RequestValues ({len(request_values)}) for VINtoCommsID query, expecting 1",
            )
        request_value = request_values[0]
        request_value_format = request_value["task:FormatType"]
        if (
            request_value_format["task:FormatOwner"] != "ETSI"
            or request_value_format["task:FormatName"] != "VIN"
        ):
            return FulfilmentOutcome(
                3007,
                f"Unexpected FormatType ({request_value_format}) for VINtoCommsID query, expecting Owner 'ETSI' and FormatType 'VIN'",
            )
        vin = str(request_value["task:Value"])
        if not self.VIN_regex.match(vin):
            return FulfilmentOutcome(
                3007,
                f"VIN ({vin}) does not match TS 103 280 clause 6.57 regex ({self.VIN_regex.pattern})",
            )
        if vin[-1].isdigit():
            expected_responses = int(vin[-1])
        else:
            expected_responses = 0
        seed = int(sha1(vin.encode("ASCII")).hexdigest(), 16)
        random.seed(seed)
        records = []
        for i in range(expected_responses):
            records.append(
                {
                    "CommsID": {
                        "EUI64": f"00:00:5e:ef:10:00:00:{random.randint(0,9)}{random.randint(0,9)}"
                    }
                }
            )
        if True:
            updatedObject = self._complete_LDRequest(obj)
        else:
            updatedObject = {}
        return_dict = {
            "VINtoCommsIDRecords" : records
        }
        return FulfilmentOutcome(updatedObject=updatedObject, records=return_dict)

    def _deliver_response(self, fulfilment_outcome, original_request, task_reference, url):
        deliver_id = str(uuid4())
        deliver_request = {
            "Header": self._copy_header_from_request(original_request),        
            "Payload": {"RequestPayload": {"ActionRequests": {"ActionRequest": [ { 
                "ActionIdentifier": 0,
                "DELIVER" :
                {
                    "Identifier" : deliver_id,
                    "HI1Object" : {
                        "@xsi:type" : "{http://uri.etsi.org/03120/common/2019/10/Delivery}DeliveryObject",
                        "ObjectIdentifier" : deliver_id,
                        "delivery:Reference" : {
                            "delivery:LDID" : task_reference,
                        },
                        "delivery:Manifest" : {
                            "delivery:Specification" : {
                                "common:Owner" : "ETSI",
                                "common:Name" : "ManifestSpecification",
                                "common:Value" : "TS103976"
                            }
                        },
                        "delivery:Delivery" : {
                            "delivery:JSONData" : fulfilment_outcome.records
                        }
                    }
                }
            }
            ]}}}}        
        deliver_request['Header']['@xmlns:delivery'] = "http://uri.etsi.org/03120/common/2019/10/Delivery"
        deliver_request['Header']['TransactionIdentifier'] = str(uuid4())
        deliver_request['Header'].pop('@xmlns:task')

        errors = self.validator.validate(deliver_request)
        if len(errors) > 0:
            raise Exception("Error validating delivery")
        r = post(url, dumps(deliver_request)) # TBD - configure timeout and error handling
        r.close()


    def respond_to(self, request: dict, context: any = {}) -> dict:
        response = self._parse_message(request, context)
        own_errors = self.validator.validate(response)
        if len(own_errors) > 0:
            logging.error(f"Failed validating own response: {own_errors}")
        return response
