from nomad_media_pip.src.helpers.send_request import _send_request

def _get_server_time(self, AUTH_TOKEN, URL, DEBUG):
    API_URL = f"{URL}/api/config/serverTime"

    return _send_request(self, AUTH_TOKEN, "Get server time", API_URL, "GET", None, None, DEBUG)