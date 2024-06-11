from nomad_media_pip.src.helpers.send_request import _send_request

def _start_live_schedule(self, AUTH_TOKEN, URL, EVENT_ID, DEBUG):
    
    API_URL = f"{URL}/api/admin/liveSchedule/content/{EVENT_ID}/start"
    
    _send_request(self, AUTH_TOKEN, "Start Live Schedule", API_URL, "POST", None, None, DEBUG) 