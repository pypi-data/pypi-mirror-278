from nomad_media_pip.src.helpers.send_request import _send_request

def _next_event(self, AUTH_TOKEN, URL, CHANNEL_ID, DEBUG):
    
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/nextEvent"
    
    return _send_request(self, AUTH_TOKEN, "Get Next Event", API_URL, "GET", None, None, DEBUG)