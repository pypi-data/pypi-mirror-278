from nomad_media_pip.src.helpers.send_request import _send_request

def _move_schedule_event(self, AUTH_TOKEN, URL, CHANNEL_ID, SCHEDULE_EVENT_ID,
                         PREVIOUS_SCHEDULE_EVENT_ID, DEBUG):
    
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/liveScheduleEvent/{SCHEDULE_EVENT_ID}/move"
    
    BODY = {
        "previousScheduleEventId": PREVIOUS_SCHEDULE_EVENT_ID
    }

    return _send_request(self, AUTH_TOKEN, "Move Schedule Event", API_URL, "PUT", None, BODY, DEBUG)