from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError
import survey
import os
import base64
from datetime import datetime

from .config_service import Config_service as configuration_service


class OAS_service:

    _api_url = "https://oaas-api.nuvem.bb.com.br/"

    _token_file_sso = "token_sso.txt"
    _token_file_platform_user = "token_plataforma.txt"

    def __init__(self):
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/69.0.3497.100 Safari/537.36"
        )
        self.token = None

    def save_token(self, filename, token):
        if token:
            file_path = os.path.join(configuration_service.module_folder, filename)
            with open(file_path, "w+") as tf:
                tf.writelines([datetime.now().isoformat() + "\n", token])

    def load_token(self, filename, timeout=None):
        token = None
        file_path = os.path.join(configuration_service.module_folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as tf:
                contents = tf.readlines()
                timediff = datetime.now() - datetime.fromisoformat(contents[0].replace("\n", ""))
                if timeout:
                    if timediff.total_seconds() < timeout:
                        token = contents[1]
                else:
                    token = contents[1]
        return token

    # ------- Token SSO -------------

    def get_sso_token(self):

        # tenta ler do arquivo
        token = self.load_token(OAS_service._token_file_sso, 60 * 30)  # 30 minutos
        if token:
            return token

        chave_f = configuration_service.get_current_user()
        sisbb_password = configuration_service.get_sisbb_password(chave_f)

        token = None

        portal_url = "https://portal.nuvem.bb.com.br/"

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(user_agent=self.user_agent)
            try:
                page = context.new_page()
                page.goto(portal_url)
                page.wait_for_timeout(2500)

                page.locator("#idToken1").first.fill(chave_f)
                page.locator("#idToken3").first.fill(sisbb_password)
                page.locator("#loginButton_0").first.click()
                two_factor = survey.routines.input("Código de autenticacao de dois fatores ou token SSO: ")
                if len(two_factor) > 6:
                    return token
                page.locator("#idToken5").first.fill(two_factor)
                page.locator("#loginButton_0").first.click()
                page.wait_for_timeout(3500)

                cookies = context.cookies()
                for cook in cookies:
                    if cook["name"] in ["BBSSOToken", "oaas_access_token"]:
                        token = cook["value"]
                        break
                context.close()
            except TimeoutError:
                print("Warning - Falha de autenticação no portal OAS, tente novamente")
                context.close()
                exit()

        self.save_token(OAS_service._token_file_sso, token)
        return token

    def get_header_sso(self):
        if not self.token:
            self.token = self.get_sso_token()
        return {"Authorization": self.token}

    # ------ usuario de plataforma -------------------

    def encode_user(self, username, password):
        b = base64.b64encode(bytes('%s:%s' % (username, password), 'utf-8'))  # bytes
        base64_str = b.decode('utf-8')  # convert bytes to string
        return f"Basic {base64_str}"

    def get_header_platform_user(self):
        if not self.token:
            self.token = self.load_token(OAS_service._token_file_platform_user)
            if not self.token:
                username = survey.routines.input("Nome do usuario de plataforma: ")
                password = survey.routines.input("Senha do usuario de plataforma: ")
                self.token = self.encode_user(username, password)
                self.save_token(OAS_service._token_file_platform_user, self.token)
        return {"Authorization": self.token}
