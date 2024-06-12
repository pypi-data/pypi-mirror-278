from nomad_media_pip.src.admin.live_operator.wait_for_live_operator_status import _wait_for_live_operator_status
from nomad_media_pip.src.helpers.send_request import _send_request

def _stop_broadcast(self, AUTH_TOKEN, URL, ID, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/{ID}/stop"

    INFO = _send_request(self, AUTH_TOKEN, "Stop Boadcast", API_URL, "POST", None, None, DEBUG)
    _wait_for_live_operator_status(self, AUTH_TOKEN, URL, ID, "Idle", 1200, 20, DEBUG)
    return INFO