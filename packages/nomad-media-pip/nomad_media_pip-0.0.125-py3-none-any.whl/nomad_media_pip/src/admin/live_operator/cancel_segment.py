from nomad_media_pip.src.helpers.send_request import _send_request

def _cancel_segment(self, AUTH_TOKEN, URL, ID, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/{ID}/cancelSegment"
    
    return _send_request(self, AUTH_TOKEN, "Cancel Segment", API_URL, "POST", None, None, DEBUG)