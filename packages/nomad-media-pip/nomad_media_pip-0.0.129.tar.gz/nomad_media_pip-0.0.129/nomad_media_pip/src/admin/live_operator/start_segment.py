from nomad_media_pip.src.helpers.send_request import _send_request

def _start_segment(self, AUTH_TOKEN, URL, ID, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/{ID}/startSegment"

    return _send_request(self, AUTH_TOKEN, "Start Segment", API_URL, "POST", None, None, DEBUG)