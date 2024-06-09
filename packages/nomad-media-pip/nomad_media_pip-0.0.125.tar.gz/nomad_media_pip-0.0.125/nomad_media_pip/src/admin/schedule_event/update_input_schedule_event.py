from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule_event.get_input_schedule_event import _get_input_schedule_event
from nomad_media_pip.src.admin.schedule_event.event_types import _EVENT_TYPES

def _update_input_schedule_event(self, AUTH_TOKEN, URL, ID, CHANNEL_ID, INPUT, BACKUP_INPUT,
                                 FIXED_ON_AIR_TIME_UTC, DEBUG):
    
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/liveScheduleEvent"
    
    SCHEDULE_EVENT_INFO = _get_input_schedule_event(self, AUTH_TOKEN, URL, CHANNEL_ID,
                                                    ID, DEBUG)

    BODY = {
        "id": ID,
        "channelId": CHANNEL_ID,
        "liveInput": INPUT or SCHEDULE_EVENT_INFO.get('input'),
        "liveInput2": BACKUP_INPUT or SCHEDULE_EVENT_INFO.get('backupInput'),
        "fixedOnAirTimeUTC": FIXED_ON_AIR_TIME_UTC or SCHEDULE_EVENT_INFO.get('fixedOnAirTimeUTC'),
        "type": {
            "id": _EVENT_TYPES["liveInput"],
            "description": "Live Input"
        }
    }

    return _send_request(self, AUTH_TOKEN, "Update Input Schedule Event", API_URL, "PUT", None, BODY, DEBUG)