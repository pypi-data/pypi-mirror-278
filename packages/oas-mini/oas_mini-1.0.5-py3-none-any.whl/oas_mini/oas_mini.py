import requests
import sys

import requests.auth

from .swagg.factory import Factory as swagg_client
from .swagg.exceptions import ValidationException
from .services.oas_service import OAS_service as oas_service


def treat_result(result: requests.Response):
    if result.status_code == 400:
        try:
            msg_data = result.json()["message"]
            if msg_data.startswith("Broker error"):
                return msg_data.split("\'")[-2]
            else:
                return msg_data
        except Exception:
            res = result.json()
            if "result" in res:
                return res["result"]
            return res
    elif result.status_code == 200:
        stuff = result.json()
        if "result" in stuff:
            return stuff["result"]
        return stuff
    elif result.status_code == 404:
        return result
    else:
        print(result.status_code)
        return result.json()


def service_url(service_name):

    env_urls = {
        "dev": "",
        "hml": "sgh.hm",
        "prd": "nuvem"
    }
    current_env = env_urls["prd"]

    if service_name == "oaas-broker-adhoc":
        return f"https://oaas-broker.{current_env}.bb.com.br/adhoc/"

    return f"https://{service_name}.{current_env}.bb.com.br/"


def return_data(message="", show_time=False):
    return {"message": message, "show_time": show_time}


def validate_service(service_name):
    services = [
        "oaas-analytics",
        "oaas-api",
        "oaas-catalogo",
        "oaas-broker",
        "oaas-broker-adhoc",
        "oas-mini"
    ]
    if service_name not in services:
        raise Exception("service not available")


def run(argument_list: list[str] = sys.argv):

    client = swagg_client("oas-mini", *argument_list)

    service_name = argument_list[0].split("/")[-1]
    validate_service(service_name)

    service = client.create_service(service_name, service_url(service_name))
    endpoint = client.get_endpoint(service)

    if endpoint:

        if swagg_client.help_flag.is_in(argument_list):
            return return_data(endpoint.help_message())

        query_arguments = client.get_query(endpoint)

        payload = client.get_file()

        if client.validate_only():
            try:
                endpoint.validate(payload, *client.args, **query_arguments)
                return return_data("Validation Succeeded. No errors found.", False)
            except ValidationException as e:
                return return_data(e, False)

        header = None
        if endpoint.header_arguments:
            header = oas_service().get_header_sso()
        elif service_name == "oaas-broker-adhoc":
            header = oas_service().get_header_platform_user()

        result = endpoint.call(service.url, header, payload, *client.args, **query_arguments)
        return return_data(treat_result(result), True)

    if swagg_client.help_flag.is_in(argument_list):
        print(f"Check out the available endpoints at: {service.url}")

    return return_data()
