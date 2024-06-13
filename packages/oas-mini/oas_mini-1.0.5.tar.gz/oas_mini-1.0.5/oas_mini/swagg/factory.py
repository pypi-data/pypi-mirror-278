import requests.auth
import requests.utils
import urllib3
import requests
import argparse
import os
import survey
import json

from .service import Service
from .endpoint import Endpoint
from .flags import BoolFlag, Flag


class Factory:

    SSL_VERIFY = False

    file_flag = Flag("--file", "-f")
    force_query_flag = BoolFlag("--force-query", "-Q")
    help_flag = BoolFlag("--help", "-h")
    query_flag = Flag("--query", "-q")
    select_flag = BoolFlag("--select", "-s")
    validation_flag = BoolFlag("--validate", "-v")

    _util_flags: list[Flag] = [
        file_flag,
        force_query_flag,
        query_flag,
        select_flag,
        validation_flag
    ]

    def get_list(lista, key):
        return lista[key] if key in lista else []

    def get_parm(parm, key):
        return parm[key] if key in parm else None

    def get_schema(route, definitions):
        params = Factory.get_list(route, "parameters")
        if params:
            payload_params = [p for p in params if p["name"] == "payload" and p["in"] == "body" and "schema" in p]
            if len(payload_params) > 0:
                payload_param = payload_params[0]
                schema_name = payload_param["schema"]["$ref"].split("/")[-1].replace("%20", " ")
                if "properties" in definitions[schema_name]:
                    return definitions[schema_name]["properties"]
        return None

    def __init__(self, name="swagg", *argument_list):
        self.parser = argparse.ArgumentParser(
            prog=name,
            description="Utilitário para fazer chamadas a endpoints swagger pela linha de comando"
        )
        for flag in Factory._util_flags:
            flag.argument_for(self.parser)
        self.subparsers = self.parser.add_subparsers(title="comandos disponíveis", required=True)
        self.args = []
        self.flag_args = {}
        if len(argument_list) < 2:
            raise Exception("Argumentos insuficientes")
        self.clargs = argument_list

    def get_subparser(self, parser: argparse.ArgumentParser):
        actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)
        ]
        return actions[0]

    def get_arguments(self, parser: argparse.ArgumentParser):
        return [
            action.dest for action in parser._actions
            if isinstance(action, argparse._StoreAction)
        ]

    def parse_recursive(self, parser: argparse.ArgumentParser, *choices):
        if len(choices) == 0:
            return parser
        choice = choices[0]
        if not parser._subparsers:
            parser.add_subparsers(dest=choice)
        subpar = self.get_subparser(parser)
        if choice not in subpar.choices:
            subpar.add_parser(choice)
        return self.parse_recursive(subpar.choices[choice], *choices[1:])

    def parse_endpoint(self, endpoint: Endpoint):
        method = endpoint.method.lower()
        if method not in self.subparsers.choices:
            self.subparsers.add_parser(method)
        command_parser = self.subparsers.choices[method]
        deeper_parser = self.parse_recursive(command_parser, *endpoint.route)
        deep_args = self.get_arguments(deeper_parser)
        for argument in endpoint.parameter_names:
            if argument not in deep_args:
                deeper_parser.add_argument(argument, nargs='?')

    def create_endpoint(self, path_name, method, parameters, query_arguments, summary, schema) -> Endpoint:

        splitted_path = [x for x in str(path_name).split("/") if x and "{" not in x]
        e = Endpoint(method, *splitted_path)

        params_in_path = [
            parm.replace("{", "").replace("}", "")
            for parm in str(path_name).split("/")
            if parm and "{" in parm
        ]
        e.set_parameters(*params_in_path)

        e.set_query_arguments(*[
            parm["name"] for parm in query_arguments if parm["in"] in ["query"]
        ])

        e.set_body(*[
            parm for parm in query_arguments if parm["in"] in ["body"]
        ])

        e.set_header_arguments(*[
            parm for parm in query_arguments if parm["in"] == "header"
        ])

        e.summary = summary
        e.schema = schema

        self.parse_endpoint(e)

        return e

    def create_endpoints(self, url) -> list[Endpoint]:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(f"{url}swagger.json", verify=Factory.SSL_VERIFY)
        serv_data = response.json()
        endpoints = []
        for path_name, routes in serv_data["paths"].items():
            endpoints += [
                self.create_endpoint(
                    path_name,
                    route_name,
                    Factory.get_list(routes, "parameters"),
                    Factory.get_list(route, "parameters"),
                    Factory.get_parm(route, "summary"),
                    Factory.get_schema(route, serv_data["definitions"])
                )
                for route_name, route in routes.items()
                if route_name.upper() in Endpoint._methods
            ]
        return endpoints

    def create_service(self, name, url) -> Service:
        ends = {e.get_key(): e for e in self.create_endpoints(url)}
        return Service(name, url, **ends)

    def get_command_key(self, subparser, *commands):
        if len(commands) < 1 or not subparser:
            return ""
        action = self.get_subparser(subparser)
        for key, value in action.choices.items():
            if key == commands[0]:
                return f"{key}/" + self.get_command_key(value._subparsers, *commands[1:])
        return ""

    def remove_method(self, key):
        return key[key.find('/') + 1:]

    def parse_route(self):
        sub = self.parser._subparsers
        endpoint_route = self.get_command_key(sub, *self.clargs[1:])
        return self.remove_method(endpoint_route)

    def parse_arguments(self, route):
        number_choices = route.count("/")
        candidate = list(self.clargs[2 + number_choices:])
        actions = [
            action for action in self.parser._subparsers._actions
            if isinstance(action, argparse._StoreAction)
            or isinstance(action, argparse._StoreTrueAction)
            or isinstance(action, argparse._HelpAction)
        ]
        for action in actions:
            for opt in action.option_strings:
                if opt in candidate:
                    idx = candidate.index(opt)
                    value = True
                    if not (isinstance(action, argparse._StoreTrueAction) or isinstance(action, argparse._HelpAction)):
                        value = candidate.pop(idx + 1)
                    candidate.pop(idx)
                    self.flag_args[opt] = value
                    continue
        return candidate

    def find_subparser(self, parser: argparse.ArgumentParser, *commands) -> argparse.ArgumentParser:
        if len(commands) < 1 or not parser._subparsers:
            return parser
        action = self.get_subparser(parser._subparsers)
        for key, value in action.choices.items():
            if key == commands[0]:
                return self.find_subparser(value, *commands[1:])
        return parser

    def get_endpoints(self, service: Service, method, route) -> list[Endpoint]:
        return [
            endpoint for key, endpoint in service.endpoints.items()
            if route == key.split()[1].split("{")[0] and method.upper() == endpoint.method
        ]

    def _create_usage_message(self, endpoint: Endpoint) -> str:
        opt_flags = []  # [flag.get_usage() for flag in [Factory.validation_flag, Factory.select_flag, Factory.help_flag]]
        if endpoint.query_argument_names:
            opt_flags.insert(0, Factory.query_flag.get_usage())
        if endpoint.schema:
            opt_flags.insert(0, Factory.file_flag.get_usage())
        options_str = " ".join(opt_flags[::-1])

        formatted_parms = endpoint.get_formatted_parameters()
        if len(formatted_parms) > 2:
            if len(options_str) > 1:
                options_str += " "
            options_str += str(formatted_parms).replace("\'", "")

        return options_str

    def _get_endpoint(self, service: Service, method, route, *arguments) -> Endpoint:

        available_endpoints = self.get_endpoints(service, method, route)
        for endpoint in available_endpoints:
            if endpoint.check_parameters(*arguments):
                return endpoint

        closest_parser = self.find_subparser(self.parser, *self.clargs[1:])
        usage_msg = closest_parser.format_usage()
        usage_msg = usage_msg.replace(self.parser.prog, service.name)
        if available_endpoints:
            available_endpoints.sort(key=lambda e: len(e.parameter_names))
            formatted = usage_msg.split("[-h]")[0][:-1]

            for endpoint in available_endpoints:
                print(formatted, self._create_usage_message(endpoint))

        if "}" in usage_msg:
            usage_msg = usage_msg.split("}")[0].replace(" [-h]", "") + "} ..."
            print(usage_msg)
        error_msg = "endpoint não localizado, verifique a rota e a quantidade de argumentos informados"
        print(service.name, method, route, *arguments, "error:", error_msg)
        exit()

    def get_endpoint(self, service: Service) -> Endpoint:

        endpoint: Endpoint = None

        if Factory.select_flag.is_in(self.clargs):
            # Let user select endpoint from list
            (keys, values) = zip(*service.endpoints.items())
            index = survey.routines.select("Selecione um endpoint: ", options=keys)
            endpoint = values[index]

        # Parse endpoint from command line
        method = self.clargs[1]
        route = self.parse_route()
        self.args = self.parse_arguments(route)
        if not endpoint:
            endpoint = self._get_endpoint(service, method, route, *self.args)
        elif not endpoint.check_parameters(*self.args):
            for param in endpoint.parameter_names[len(self.args):]:
                self.args.append(survey.routines.input(f"{param}: "))
        return endpoint

    def get_flag_argument(self, flag: Flag):
        for name in flag.names:
            if name in self.flag_args:
                return self.flag_args[name]
        return flag.default

    def get_query(self, endpoint):
        filename = self.get_flag_argument(Factory.query_flag)
        missing_qa = [qa for qa in endpoint.query_argument_names]
        result = {}
        if filename:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    content_dict = json.loads(f.read())
                    for k, v in content_dict.items():
                        if k not in missing_qa:
                            if Factory.force_query_flag.is_in(self.clargs):
                                result[k] = v
                            else:
                                print(f"Warning: {k} does not seem to be a valid query argument. Ignored.")
                        else:
                            missing_qa.remove(k)
                            result[k] = v
        for qa in missing_qa:
            result[qa] = survey.routines.input(qa + ": ")
        return result

    def get_file(self):
        filename = self.get_flag_argument(Factory.file_flag)
        if filename:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    contents = f.read()
                    if contents:
                        return json.loads(contents)
        return None

    def validate_only(self):
        return self.get_flag_argument(Factory.validation_flag)
