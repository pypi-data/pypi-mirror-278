from nomad_media_pip.src.helpers.send_request import _send_request 

def _ping(self, AUTH_TOKEN, URL, APPLICATION_ID, USER_SESSION_ID, DEBUG):
        
    API_URL = f"{URL}/api/account/ping"

    BODY = {
        "userSessionId": USER_SESSION_ID
    }

    if (APPLICATION_ID):
        BODY["applicationId"] = APPLICATION_ID

    return _send_request(self, AUTH_TOKEN, "Ping", API_URL, "POST", None, BODY, DEBUG)
    