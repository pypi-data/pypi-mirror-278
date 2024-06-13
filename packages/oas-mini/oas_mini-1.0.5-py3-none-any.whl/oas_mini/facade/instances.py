import argparse
from datetime import datetime, timedelta
from tabulate import tabulate

from ..utils.facade import FacadeHelper
from ..services.config_service import Config_service


def instances(argument_list):

    parser = argparse.ArgumentParser()
    parser.add_argument("quantity", nargs="?", default=5, type=int)
    args = parser.parse_args(argument_list)
    amount = vars(args)["quantity"]

    user_key = Config_service.get_current_user()
    query = {
        "small": "true",
        "state": "PROVISIONED,DEPROVISION_FAIL,DEPROVISIONING",
        "context.user_id": user_key,
        "page_size": amount,
        "sort": -1
    }

    result = FacadeHelper.run(["oaas-api", "get", "instance", "sorted", "parents", "--force-query"], query_data=query)

    if len(result["message"]) > 0:
        headers = ["Nome Identificador", "Data solicitação", "Tipo", "URL"]
        instances = []
        for instance in result["message"]:
            start_time = datetime.fromisoformat(instance["provision_dates"]["start"]) - timedelta(hours=3)
            instance_data = [
                instance["context"]["tag_name"],
                start_time.strftime("%d/%m/%Y %H:%M:%S"),
                instance["offer"]["displayName"],
                "https://portal.nuvem.bb.com.br/view-instance/" + instance["instance_id"]
            ]
            instances.append(instance_data)
        return "\n" + tabulate(instances, headers) + "\n"

    return result["message"]
