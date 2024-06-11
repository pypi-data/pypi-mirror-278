from nomad_media_pip.src.helpers.send_request import _send_request

def _get_user_session(self, AUTH_TOKEN, URL, API_TYPE, USER_ID, DEBUG):

    API_URL = f"{URL}/api/admin/user-session/{USER_ID}" if API_TYPE == "admin" else f"{URL}/api/user-session/{USER_ID}"

    return _send_request(self, AUTH_TOKEN, "Get User Session", API_URL, "GET", None, None, DEBUG)