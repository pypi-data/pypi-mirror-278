from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_operator(self, AUTH_TOKEN, URL, ID, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/{ID}"

    return _send_request(self, AUTH_TOKEN, "Getting Live Operator {ID}", API_URL, "GET", None, None, DEBUG)