from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_operators(self, AUTH_TOKEN, URL, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator"

    return _send_request(self, AUTH_TOKEN, "Getting Live Operators", API_URL, "GET", None, None, DEBUG)