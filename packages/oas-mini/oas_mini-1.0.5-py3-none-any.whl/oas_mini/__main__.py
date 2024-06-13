import argparse
import os
from datetime import datetime

from .utils.helper import format_seconds_to_hms
from .oas_mini import run
from .utils.facade import FacadeHelper
from .services.config_service import Config_service


def main():

    start_time = datetime.now()

    result = run()
    print(result["message"])

    if result["show_time"]:
        finish_time = datetime.now()
        time_spent = finish_time - start_time
        print(f"Done! time spent: {format_seconds_to_hms(time_spent.total_seconds())}")


def facade():
    start_time = datetime.now()

    parser = argparse.ArgumentParser(
        prog="oas-mini",
        description="Utilitário para executar ações do portal OAS via linha de comando."
    )

    # module_folder = sys.modules[__name__].__file__.replace("__main__.py", "")
    facade_directory = os.path.join(Config_service.module_folder, "facade")
    choices = [
        entry.name.replace(".py", "")
        for entry in os.scandir(facade_directory)
        if entry.is_file() and ".py" in entry.name and "__" not in entry.name
    ]
    parser.add_argument("action_name", choices=choices)

    args, leftovers = parser.parse_known_args()
    args = vars(args)
    action_name = args["action_name"]

    result = FacadeHelper.call_facade(action_name, leftovers)
    print(result)

    finish_time = datetime.now()
    time_spent = finish_time - start_time
    print(f"Done! time spent: {format_seconds_to_hms(time_spent.total_seconds())}")


if __name__ == '__main__':
    main()
