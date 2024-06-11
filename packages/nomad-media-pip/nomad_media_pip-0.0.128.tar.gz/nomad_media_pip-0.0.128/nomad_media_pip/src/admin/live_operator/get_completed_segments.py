from nomad_media_pip.src.helpers.send_request import _send_request

def _get_completed_segments(self, AUTH_TOKEN, URL, ID, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/{ID}/segments"

    return _send_request(self, AUTH_TOKEN, "Getting completed segments for Live Channel {ID}", API_URL, "GET", None, None, DEBUG)