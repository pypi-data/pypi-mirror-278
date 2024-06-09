from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule_event.event_types import _EVENT_TYPES

def _add_input_schedule_event(self, AUTH_TOKEN, URL, CHANNEL_ID, INPUT, BACKUP_INPUT, 
                              ON_AIR_TIME, PREVIOUS_ID, DEBUG):
    API_URL = f"{URL}/api/liveChannel/" + CHANNEL_ID + "/liveScheduleEvent"
    
    # Build the payload BODY
    BODY = {
        "channelId": CHANNEL_ID,
        "fixedOnAirTimeUtc": ON_AIR_TIME,
        "type": {
            "id": _EVENT_TYPES["liveInput"],
            "description": "Live Input"
        },
        "liveInput": INPUT,
        "previousId": PREVIOUS_ID
    }

    return _send_request(self, AUTH_TOKEN, "Add Input Schedule Event", API_URL, "POST\nBODY: {json.dumps(BODY", None, BODY, DEBUG)