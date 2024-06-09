from nomad_media_pip.src.helpers.send_request import _send_request

def _login(self, URL, USERNAME, PASSWORD, DEBUG):
        
    API_URL = f"{URL}/api/account/login"

    BODY = {
        "username": USERNAME,
        "password": PASSWORD
    }

    return _send_request(self, None, "Login", API_URL, "POST", None, BODY, DEBUG)    