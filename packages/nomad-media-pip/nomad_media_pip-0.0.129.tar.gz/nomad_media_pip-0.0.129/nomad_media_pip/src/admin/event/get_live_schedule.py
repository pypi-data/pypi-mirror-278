from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_schedule(self, AUTH_TOKEN, URL, EVENT_ID, DEBUG):

    API_URL = f"{URL}/api/admin/liveSchedule/content/{EVENT_ID}"
    
    _send_request(self, AUTH_TOKEN, "Get Live Schedule", API_URL, "GET", None, None, DEBUG) 