from nomad_media_pip.src.helpers.send_request import _send_request

def _get_asset_schedule_event(self, AUTH_TOKEN, URL, CHANNEL_ID, SCHEDULE_EVENT_ID, DEBUG):
        
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/liveScheduleEvent/{SCHEDULE_EVENT_ID}"
    
    return _send_request(self, AUTH_TOKEN, "Get Asset Schedule Event", API_URL, "GET", None, None, DEBUG)