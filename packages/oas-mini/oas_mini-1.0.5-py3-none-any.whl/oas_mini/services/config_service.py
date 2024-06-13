import os
import re
import survey
import sys
import subprocess


class Config_service:

    SSL_VERIFY = False  # bool(os.environ.get("REQUESTS_CA_BUNDLE"))

    module_folder = sys.modules[__name__].__file__.replace("services/config_service.py", "")

    #  --------- user credentials for this enviroment -----------

    def validate_userkey(key):
        return key[0] in ["c", "f", "C", "F"] and len(key) == 8 and key[1:].isnumeric()

    def validate_password(key):
        return len(key) == 8 and key.isnumeric()

    def get_current_user():
        # tenta pegar chave do email do usuário do git
        git_mail = subprocess.run(args=["git", "config", "user.email", ], capture_output=True)
        mailname = git_mail.stdout.decode().split("@")[0].lower()
        if Config_service.validate_userkey(mailname):
            return mailname

        # tenta pegar chave da variavel de ambiente do windows
        try:
            cmd_user = subprocess.run(args=["cmd.exe", "/c", "echo", "%USERNAME%"], capture_output=True)
            return cmd_user.stdout.decode().replace('\r', '').replace('\n', '').lower()
        except Exception:
            print("Warning - Failed to get user credentials from enviroment variables")

        # pede ao usuário pra digitar a chave
        while True:
            key = survey.routines.input("Por favor insira sua chave funci: ")
            if Config_service.validate_userkey(key):
                return key
            print("chave inválida")

    def get_sisbb_password(chave_f):
        # try getting password from pengwin
        contents = ""
        pattern = r"export http_proxy=\"http:\/\/" + chave_f + r":(\d+)@\$ipProxy:\$portaProxy\""
        with open(os.path.expanduser("~/.local/bin/carrega-proxy"), "r") as peng_file:
            contents = peng_file.read()
        search = re.findall(pattern, contents)
        if len(search) > 0:
            return search[0]
        with open("/etc/proxychains.conf", "r") as peng_file:
            contents = peng_file.read()
        search = contents.split()[-1]
        if Config_service.validate_password(search):
            return search
        while True:
            key = survey.routines.conceal("Por favor insira sua senha sisBB: ")
            if Config_service.validate_password(key):
                return key
            print("chave inválida")
