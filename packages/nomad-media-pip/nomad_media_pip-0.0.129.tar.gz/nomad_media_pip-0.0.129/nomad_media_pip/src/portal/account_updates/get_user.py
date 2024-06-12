from nomad_media_pip.src.helpers.send_request import _send_request

def _get_user(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/api/account/user"

    return _send_request(self, AUTH_TOKEN, "Get user", API_URL, "GET", None, None, DEBUG)