import argparse

from ..utils.facade import FacadeHelper


def approve(argument_list):

    parser = argparse.ArgumentParser()
    parser.add_argument("waiting_id")
    args = parser.parse_args(argument_list)
    instance_data = vars(args)

    payload = {}
    payload["access_name"] = ".*"

    # obtain method type
    result = FacadeHelper.run(["oaas-api", "get", "instance", "waiting", instance_data["waiting_id"]], file_data=payload)
    request_type = result["message"]["request_type"]
    request_methods = {
        "provision": "put",
        "deprovision": "delete",
        "default": "patch"
    }
    if request_type not in request_methods:
        request_type = "default"
    method = request_methods[request_type]

    # approve
    result = FacadeHelper.run(["oaas-api", method, "instance", "waiting", instance_data["waiting_id"]], file_data=payload)

    if len(result["message"]) > 0:
        if "instance_id" in result["message"][0]:
            return "URL para visualizar a instância:\n\rhttps://portal.nuvem.bb.com.br/view-instance/" + result["message"][0]["instance_id"]

    return result["message"]
