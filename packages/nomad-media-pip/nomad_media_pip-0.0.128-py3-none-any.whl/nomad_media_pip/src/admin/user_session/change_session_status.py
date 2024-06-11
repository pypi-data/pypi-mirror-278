from nomad_media_pip.src.helpers.send_request import _send_request

def _change_session_status(self, AUTH_TOKEN, URL, USER_ID, USER_SESSION_STATUS, 
                          APPLICATION_ID, DEBUG):

    API_URL = f"{URL}/api/admin/user-session"
    
    BODY = {
        "id": USER_ID,
        "userSessionStatus": USER_SESSION_STATUS,
        "applicationId": APPLICATION_ID
    }

    return _send_request(self, AUTH_TOKEN, "Change Session Status", API_URL, "POST", None, BODY, DEBUG)