import importlib
import json
import os
import re
import requests
import survey

from ..swagg.factory import Factory
from ..oas_mini import run
from ..services.config_service import Config_service


class FacadeHelper:

    # --- User Input ---

    def ask_user_confirmation():
        continuar = survey.routines.inquire("Are you sure? ", default=False)
        if not continuar:
            print("Aborted by user")
            exit()

    def ask_group():
        try:
            groups = FacadeHelper.run(["oaas-api", "get", "group"])
            groups = groups["message"]
            group_ids = {group["name"]: group["id"] for group in groups}
            group_names = list(group_ids.keys())
            group_index = survey.routines.select("grupo*: ", options=group_names)
            group_name = group_names[group_index]
            return group_ids[group_name]
        except Exception as e:
            print("Error - Unable to fetch group data, probably due to an authentication failure. A retry is recommended.")
            raise e

    # --- Output Treatment ---

    def wait_approval_msg(result) -> str:
        user_msg = result["message"]["msg"] + ". Id: " + result["message"]["id"]
        return user_msg

    # --- Offer Input Fields ---

    def build_question(input_def):
        question = input_def["name"]
        if "required" in input_def and input_def["required"] == "true":
            question += "*"
        return question + ": "

    def get_input_string(offer_name, offer_major, plan, input_def):
        question = FacadeHelper.build_question(input_def)
        answer = survey.routines.input(question)
        return answer

    def get_input_select(offer_name, offer_major, plan, input_def):
        question = FacadeHelper.build_question(input_def)
        opts = {}
        if "values_from_url" in input_def:
            try:
                query_data = {
                    "offer": "stable"
                }
                values_response = FacadeHelper.run(
                    ["oaas-catalogo", "get", "util", "values_from_url", offer_name, offer_major, plan, input_def["name"]],
                    query_data=query_data
                )
                # opts = requests.get(input_def["values_from_url"], verify=Factory.SSL_VERIFY)
                opts = values_response["message"]
            except requests.exceptions.ConnectionError:
                print("Falha ao obter opções para o parâmetro " + input_def["name"] + " a partir da url.")
                exit(1)
        elif "values_from_list" in input_def:
            opts = {value["label"]: value["value"] for value in input_def["values_from_list"]}
        opt_labels = list(opts.keys())
        opt_index = survey.routines.select(question, options=opt_labels)
        label = opt_labels[opt_index]
        return opts[label]

    def get_input_secure(offer_name, offer_major, plan, input_def):
        question = FacadeHelper.build_question(input_def)
        return survey.routines.conceal(question)

    def get_input_bool(offer_name, offer_major, plan, input_def):
        question = FacadeHelper.build_question(input_def)
        default_value = True
        if "default" in input_def and input_def["default"] == "false":
            default_value = False
        return survey.routines.inquire(question, default=default_value)

    def get_input_float(offer_name, offer_major, plan, input_def):
        question = FacadeHelper.build_question(input_def)
        answer = survey.routines.input(question)
        return float(answer)

    def get_input_hidden(offer_name, offer_major, plan, input_def):
        return None

    def get_input_int(offer_name, offer_major, plan, input_def):
        question = FacadeHelper.build_question(input_def)
        answer = survey.routines.input(question)
        return int(answer)

    def get_input_list(offer_name, offer_major, plan, input_def):
        answers = []
        while True:
            answer = FacadeHelper.get_input_string(offer_name, offer_major, plan, input_def)
            if not answer or answer == "":
                break
            answers.append(answer)
        return answers

    _input_types = {
        "boolean": get_input_bool,
        "card": get_input_select,
        "float": get_input_float,
        "hidden": get_input_hidden,
        "integer": get_input_int,
        "json_object": get_input_string,
        "list_object": get_input_list,
        "secure": get_input_secure,
        "secure_encrypt": get_input_secure,
        "select": get_input_select,
        "sigla_almfe": get_input_string,  # Lista pro usuario selecionar!
        "sigla_almfd": get_input_string,  # Lista pro usuario selecionar!
        "sigla_dados": get_input_string,  # Lista pro usuario selecionar!
        "string": get_input_string,
        "textarea": get_input_string,
    }

    def get_input_value(offer_name, offer_major, plan, input_def):
        value = FacadeHelper._input_types[input_def["type"]](offer_name, offer_major, plan, input_def)
        if (value == "" or value is None) and "default" in input_def:
            value = input_def["default"]
        if "validate" in input_def:
            if (value == "" or value is None) and ("required" not in input_def or input_def["required"] == "false"):
                return None
            if not re.match(input_def["validate"], value):
                if "validate_msg" in input_def:
                    print(input_def["validate_msg"])
                else:
                    print("Valor inválido, precisa satisfazer o regex: \"" + input_def["validate"] + "\"")
                return FacadeHelper._input_types[input_def["type"]](offer_name, offer_major, plan, input_def)
        return value

    # --- Payload ---

    temp_file_name = os.path.join(Config_service.module_folder, "temp_file.json")

    def save_json_to_temp_file(data):
        with open(FacadeHelper.temp_file_name, "w") as temp_file:
            json.dump(data, temp_file)

    def delete_temp_file():
        if os.path.isfile(FacadeHelper.temp_file_name):
            os.remove(FacadeHelper.temp_file_name)

    # --- Query ---

    temp_query_file_name = os.path.join(Config_service.module_folder, "temp_query.json")

    def save_query(data):
        with open(FacadeHelper.temp_query_file_name, "w") as temp_file:
            json.dump(data, temp_file)

    def delete_query():
        if os.path.isfile(FacadeHelper.temp_query_file_name):
            os.remove(FacadeHelper.temp_query_file_name)

    # --- Run ---

    def run(argument_list, file_data=None, query_data=None):
        if file_data:
            FacadeHelper.save_json_to_temp_file(file_data)
            argument_list += [Factory.file_flag.name, FacadeHelper.temp_file_name]
        if query_data:
            FacadeHelper.save_query(query_data)
            argument_list += [Factory.query_flag.name, FacadeHelper.temp_query_file_name]
        result = run(argument_list)
        FacadeHelper.delete_temp_file()
        FacadeHelper.delete_query()
        return result

    def call_facade(action, args):
        module = importlib.import_module(f".facade.{action}", package="oas_mini")
        method_to_call = getattr(module, action)
        return method_to_call(args)
