import argparse
import survey

from ..services.config_service import Config_service
from ..utils.facade import FacadeHelper


def provision(argument_list):

    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-approve", "-a", action="store_true")

    parser.add_argument("offer_name")
    parser.add_argument("offer_major", type=int)
    parser.add_argument("quantity", nargs="?", default=1, type=int)
    args = parser.parse_args(argument_list)
    offer_data = vars(args)

    auto_approve = offer_data.pop("auto_approve", False)

    # get offer info
    offer = FacadeHelper.run(["oaas-catalogo", "get", "offer", offer_data["offer_name"], str(offer_data["offer_major"])])
    if not offer["message"]:
        return "Offer not found."
    offer = offer["message"][0]

    # prompt for group
    group_id = FacadeHelper.ask_group()

    # user must select a plan
    plans = {plan["name"]: plan for plan in offer["manifest"]["plans"]}
    plan_names = list(plans.keys())
    plan_index = survey.routines.select("plano*: ", options=plans.keys())
    offer_data["plan"] = plan_names[plan_index]
    selected_plan = plans[offer_data["plan"]]

    # prompt for the necessary inputs
    offer_data["inputs"] = {}
    for user_input in selected_plan["inputs"]:
        input_value = FacadeHelper.get_input_value(
            offer_data["offer_name"],
            str(offer_data["offer_major"]),
            offer_data["plan"],
            user_input
        )
        if input_value:
            offer_data["inputs"][user_input["name"]] = input_value

    # fill in the context
    offer_data["context"] = {
        "user_id": Config_service.get_current_user(),
        "group_id": group_id
    }

    result = FacadeHelper.run(["oaas-api", "put", "instance"], file_data=offer_data)

    if "msg" in result["message"]:
        if "id" in result["message"]:
            app_msg = FacadeHelper.wait_approval_msg(result)
            if auto_approve:
                print(app_msg)
                print("Tentando realizar aprovação automática...")
                waiting_id = app_msg.split()[-1]
                result = FacadeHelper.call_facade("approve", [waiting_id])
                return result
            return app_msg
        elif "instance" in result["message"]:
            user_msg = result["message"]["msg"]
            user_msg += ".\nURL da instância: https://portal.nuvem.bb.com.br/view-instance/"
            user_msg += result["message"]["instance"]
            return user_msg

    return result["message"]
