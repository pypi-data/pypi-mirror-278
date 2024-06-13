import argparse

from ..utils.facade import FacadeHelper


def deprovision(argument_list):

    FacadeHelper.ask_user_confirmation()

    parser = argparse.ArgumentParser()
    parser.add_argument("--auto-approve", "-a", action="store_true")

    parser.add_argument("instance_id")
    args = parser.parse_args(argument_list)
    instance_data = vars(args)

    auto_approve = instance_data.pop("auto_approve", False)

    instance = FacadeHelper.run(["oaas-api", "get", "instance", instance_data["instance_id"]], query_data={"small": "false"})

    if not instance["message"]:
        return "Unable to find instance, make sure the instance_id is correct."

    instance_data["offer_name"] = instance["message"]["offer"]["name"]
    instance_data["offer_major"] = instance["message"]["offer"]["major"]
    instance_data["plan"] = instance["message"]["plan"]["id"]

    result = FacadeHelper.run(["oaas-api", "delete", "instance"], file_data=instance_data)

    if "msg" in result["message"]:
        app_msg = FacadeHelper.wait_approval_msg(result)
        if auto_approve:
            print(app_msg)
            print("Tentando realizar aprovação automática...")
            waiting_id = app_msg.split()[-1]
            result = FacadeHelper.call_facade("approve", [waiting_id])
            return result
        return app_msg

    return result["message"]
