from nomad_media_pip.src.helpers.send_request import _send_request

def _logout(self, AUTH_TOKEN, URL, USER_SESSION_ID, DEBUG):
    API_URL = f"{URL}/api/account/logout"

    BODY = {
        "userSessionId": USER_SESSION_ID,   
    }

    return _send_request(self, AUTH_TOKEN, "Logout", API_URL, "POST", None, BODY, DEBUG)    