from nomad_media_pip.src.helpers.send_request import _send_request

def _refresh_token(self, AUTH_TOKEN, URL, REFRESH_TOKEN, DEBUG):
    API_URL = f"{URL}/api/account/refresh-token"

    BODY = {
        "refreshToken": REFRESH_TOKEN
    }

    TOKEN_INFO = _send_request(None, AUTH_TOKEN, "Refresh Token", API_URL, "POST", None, BODY, DEBUG)    

    self.token = TOKEN_INFO["token"]

    return TOKEN_INFO["token"]