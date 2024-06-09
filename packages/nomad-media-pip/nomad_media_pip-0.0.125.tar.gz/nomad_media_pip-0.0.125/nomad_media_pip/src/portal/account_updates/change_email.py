from nomad_media_pip.src.helpers.send_request import _send_request 

def _change_email(self, AUTH_TOKEN, URL, EMAIL, PASSWORD, DEBUG):
  
    API_URL = f"{URL}/api/account/change-email"

    BODY = {
        "password": PASSWORD,
        "newEmail": EMAIL
    }

    return _send_request(self, AUTH_TOKEN, "Change email", API_URL, "POST", None, BODY, DEBUG)
    