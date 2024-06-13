import math
import requests

from .exceptions import ValidationException


class Endpoint:

    _methods = [
        "GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"
    ]

    _representation = {
        "object": "{}",
        "string": "\"string\"",
        "number": "0"
    }

    _py_types = {
        "object": dict,
        "string": str,
        "number": int
    }

    def get_representation(data_type):
        return Endpoint._representation[data_type]

    def __init__(self, method: str, *route):
        self.method = method.upper()
        if self.method not in Endpoint._methods:
            raise Exception("method not available")
        self.route = route
        self.summary = None
        self.parameter_names = []
        self.query_argument_names = []
        self.header_arguments = []
        self.payload = None
        self.schema = None

    # --- get/set ---------------------------------

    def set_parameters(self, *names):
        self.parameter_names = names

    def set_body(self, *content):
        if len(content) == 1:
            self.payload = content[0]

    def set_query_arguments(self, *names):
        self.query_argument_names = names

    def set_header_arguments(self, *names):
        self.header_arguments = names

    def get_key(self):
        joined_route = "/".join(self.route)
        joined_parms = "/".join(["{" + pn + "}" for pn in self.parameter_names])
        return self.method + " " + joined_route + "/" + joined_parms

    def get_formatted_parameters(self):
        if len(self.parameter_names) == 0:
            return "()"
        elif len(self.parameter_names) == 1:
            return "({})".format(self.parameter_names[0])
        else:
            return str(self.parameter_names).replace("\'", "")

    # --- validations ---------------------------

    def check_parameters(self, *parameters):
        return len(parameters) == len(self.parameter_names)

    def validate_parameters(self, *parameters):
        if not self.check_parameters(*parameters):
            raise ValidationException("Wrong number of parameters for endpoint")

    def validate_query(self, **query_args):
        for argname, _ in query_args.items():
            if argname not in self.query_argument_names:
                raise ValidationException(f"Query argument {argname} does not exist for this endpoint")

    def validate_schema(self, payload):
        if self.schema:
            if not payload:
                print("Warning - Payload is missing, unable to validate")
            else:
                for parameter_name, value in payload.items():
                    expected_type = self.schema[parameter_name]["type"]
                    if not isinstance(value, Endpoint._py_types[expected_type]):
                        e_msg = f"Payload content does not match the schema required: {parameter_name} should be {expected_type}"
                        raise ValidationException(e_msg)

    def validate(self, body=None, *parameters, **query_args):
        self.validate_parameters(*parameters)
        self.validate_query(**query_args)
        self.validate_schema(body)

    # --- call -----------------------------------

    def call(self, base_url, header=None, body=None, *parameters, **query_args):

        self.validate_parameters(*parameters)
        url = base_url + "/".join(self.route)
        if parameters:
            url += "/" + "/".join(parameters)
        if query_args:
            url += "?" + "&".join([f"{k}={v}" for k, v in query_args.items() if len(str(v)) > 0])

        if not parameters and not query_args and not url.endswith("/"):  # this is a bug fix
            url += "/"

        try:
            return requests.request(self.method, url, headers=header, verify=False, json=body)
        except requests.exceptions.ConnectionError as connection_error:
            print("Connection Error")
            raise connection_error

    def help_message(self):
        message = "\n" + self.get_key()
        if self.summary:
            message += "\n" + self.summary
        if self.query_argument_names:
            message += "\n\n" + "-- query parameters --"
            for qa in self.query_argument_names:
                message += "\n" + qa
        if self.schema:
            message += "\n\n" + "-- payload schema --"
            message += "\n" + "{"
            representations = {
                f"\n\t\"{p_name}\": " + Endpoint.get_representation(p_data["type"]): "# " + p_data["description"]
                for p_name, p_data in self.schema.items()
            }
            lengths = {key: len(key) for key in representations.keys()}
            max_length = max(lengths.values())
            tabs = {key: ["\t"] * (1 + math.ceil((max_length - length) / 8)) for key, length in lengths.items()}
            for representation, description in representations.items():
                message += representation + "," + "".join(tabs[representation]) + description
            message += "\n" + "}"
        return message + "\n"
