from nomad_media_pip.src.helpers.send_request import _send_request

def _cancel_broadcast(self, AUTH_TOKEN, URL, ID, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/{ID}/cancel"

    return _send_request(self, AUTH_TOKEN, "Cancel Broadcast", API_URL, "POST", None, None, DEBUG)