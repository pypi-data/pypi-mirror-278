import json
from pathlib import Path
import logging
from itertools import chain
from importlib import resources
from . import schemas

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


class JsonValidator:
    def __init__(self, core_schema, other_schemas):
        self._core_schema = json.load(core_schema.open())
        self._schema_dict = {self._core_schema["$id"]: self._core_schema}
        self._supporting_paths = []
        for thing in other_schemas:
            path = Path(thing)
            if path.is_dir():
                logging.debug(f"Searching {path} for schema files")
                self._supporting_paths.extend(path.rglob("*.schema.json"))
            else:
                logging.debug(f"Appending {path} as schema file")
                self._supporting_paths.append(path)
        logging.info(f"Supporting schema paths: {self._supporting_paths}")
        self._supporting_schemas = [json.load(p.open()) for p in self._supporting_paths]
        self._schema_dict = self._schema_dict | {
            s["$id"]: s for s in self._supporting_schemas
        }
        logging.info(f"Loaded schema IDs: {[k for k in self._schema_dict.keys()]}")
        # self._resolver = RefResolver(None,
        #                 referrer=None,
        #                 store=self._schema_dict)
        # logging.info("Created RefResolver")
        self._registry = Registry().with_resources(
            [
                (k, Resource(contents=v, specification=DRAFT202012))
                for k, v in self._schema_dict.items()
            ]
        )
        self._validator = Draft202012Validator(
            self._core_schema, registry=self._registry
        )
        logging.info("Created validator")

    def validate(self, instance_doc: str):
        errors = list(self._validator.iter_errors(instance_doc))
        return errors


class TS103120Validator(JsonValidator):
    def __init__(self):
        repo_path = resources.files(schemas).joinpath("dummy").parent  # Hack
        schema_dirs = [repo_path]
        core_schema = repo_path / "ts_103120_Core.schema.json"
        JsonValidator.__init__(self, core_schema, schema_dirs)
        request_fragment_schema = {
            "$ref": "ts_103120_Core_2019_10#/$defs/RequestPayload"
        }
        self._request_fragment_validator = Draft202012Validator(
            request_fragment_schema, registry=self._registry
        )
        response_fragment_schema = {
            "$ref": "ts_103120_Core_2019_10#/$defs/ResponsePayload"
        }
        self._response_fragment_validator = Draft202012Validator(
            response_fragment_schema, registry=self._registry
        )

    def expand_request_response_exception(self, ex):
        if list(ex.schema_path) == ["properties", "Payload", "oneOf"]:
            logging.info(
                "Error detected validating payload oneOf - attempting explicit validation..."
            )
            if "RequestPayload" in self.instance_doc["Payload"].keys():
                ret_list = list(
                    chain(
                        *[
                            self.expand_action_exception(x)
                            for x in self._request_fragment_validator.iter_errors(
                                self.instance_doc["Payload"]["RequestPayload"]
                            )
                        ]
                    )
                )
                for r in ret_list:
                    r.path = ex.path + r.path
                return ret_list
            elif "ResponsePayload" in self.instance_doc["Payload"].keys():
                ret_list = list(
                    chain(
                        *[
                            self.expand_action_exception(x)
                            for x in self._request_fragment_validator.iter_errors(
                                self.instance_doc["Payload"]["ResponsePayload"]
                            )
                        ]
                    )
                )
                for r in ret_list:
                    r.path = ex.path + r.path
                return ret_list
            else:
                logging.error(
                    "No RequestPayload or ResponsePayload found - is the Payload malformed?"
                )
                return [ex]
        else:
            return [ex]

    def expand_action_exception(self, ex):
        logging.error("Error detected in ActionRequests/ActionResponses")
        error_path = list(ex.schema_path)
        if error_path != [
            "properties",
            "ActionRequests",
            "properties",
            "ActionRequest",
            "items",
            "allOf",
            1,
            "oneOf",
        ] and error_path != [
            "properties",
            "ActionResponses",
            "properties",
            "ActionResponse",
            "items",
            "allOf",
            1,
            "oneOf",
        ]:
            logging.error("Error not in inner Request/Response allOf/oneOf constraint")
            return [ex]
        j = ex.instance
        j.pop(
            "ActionIdentifier"
        )  # Remove ActionIdentifier - one remaining key will be the verb
        verb = list(j.keys())[0]
        message = "Request" if error_path[1] == "ActionRequests" else "Response"
        v = Draft202012Validator(
            {"$ref": f"ts_103120_Core_2019_10#/$defs/{verb}{message}"},
            registry=self._registry,
        )
        ret_list = list(
            chain(*[self.expand_object_exception(x) for x in v.iter_errors(j[verb])])
        )
        for r in ret_list:
            r.path = ex.path + r.path
        return ret_list

    def expand_object_exception(self, ex):
        logging.error("Error detected in verb")
        # The final level of validation is for the actual HI1Object validation
        if list(ex.schema_path) != ["properties", "HI1Object", "oneOf"]:
            logging.error("Error not inside HI1Object")
            return [ex]
        object_type = ex.instance["@xsi:type"].split("}")[-1]
        object_ref = {
            "AuthorisationObject": "ts_103120_Authorisation_2020_09#/$defs/AuthorisationObject",
            "LITaskObject": "ts_103120_Task_2020_09#/$defs/LITaskObject",
            "LDTaskObject": "ts_103120_Task_2020_09#/$defs/LDTaskObject",
            "LPTaskObject": "ts_103120_Task_2020_09#/$defs/LPTaskObject",
            "DocumentObject": "ts_103120_Document_2020_09#/$defs/DocumentObject",
            "NotificationObject": "ts_103120_Notification_2016_02#/$defs/NotificationObject",
            "DeliveryObject": "ts_103120_Delivery_2019_10#/$defs/DeliveryObject",
            "TrafficPolicyObject": "ts_103120_TrafficPolicy_2022_07#/$defs/TrafficPolicyObject",
            "TrafficRuleObject": "ts_103120_TrafficPolicy_2022_07#/$defs/TrafficRuleObject",
        }[object_type]
        v = Draft202012Validator({"$ref": object_ref}, registry=self._registry)
        print(ex.instance)
        print(object_ref)
        return list(v.iter_errors(ex.instance))

    def validate(self, instance_doc: str):
        errors = JsonValidator.validate(self, instance_doc)
        self.instance_doc = instance_doc
        out_errors = list(
            chain(*[self.expand_request_response_exception(ex) for ex in errors])
        )
        return out_errors
        return errors
