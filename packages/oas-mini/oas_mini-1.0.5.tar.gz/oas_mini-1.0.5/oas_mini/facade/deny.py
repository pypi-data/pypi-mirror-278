import argparse
import survey

from ..utils.facade import FacadeHelper


def deny(argument_list):

    parser = argparse.ArgumentParser()
    parser.add_argument("waiting_id")
    args = parser.parse_args(argument_list)
    instance_data = vars(args)

    # get reason
    payload = {}
    payload["reason"] = survey.routines.input("Informe o motivo: ")

    result = FacadeHelper.run(["oaas-api", "post", "instance", "waiting", instance_data["waiting_id"]], file_data=payload)

    return result["message"]
