from nomad_media_pip.src.helpers.send_request import _send_request 

def _change_password(self, AUTH_TOKEN, URL, CURRENT_PASSWORD, NEW_PASSWORD, DEBUG):
  
    API_URL = f"{URL}/api/account/change-password"

    BODY = {
        "password": CURRENT_PASSWORD,
        "newPassword": NEW_PASSWORD
    }

    return _send_request(self, AUTH_TOKEN, "Change password", API_URL, "POST", None, BODY, DEBUG)
    