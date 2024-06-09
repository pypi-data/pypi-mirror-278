from nomad_media_pip.src.helpers.send_request import _send_request

def _stop_live_schedule(self, AUTH_TOKEN, URL, EVENT_ID, DEBUG):

    API_URL = f"{URL}/api/admin/liveSchedule/content/{EVENT_ID}/stop"
    
    _send_request(self, AUTH_TOKEN, "Stop Live Schedule", API_URL, "POST", None, None, DEBUG) 