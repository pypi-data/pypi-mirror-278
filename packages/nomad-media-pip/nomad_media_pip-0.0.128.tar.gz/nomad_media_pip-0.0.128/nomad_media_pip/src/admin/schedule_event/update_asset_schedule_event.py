from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule_event.event_types import _EVENT_TYPES
from nomad_media_pip.src.admin.schedule_event.get_asset_schedule_event import _get_asset_schedule_event

def _update_asset_schedule_event(self, AUTH_TOKEN, URL, ID, CHANNEL_ID, ASSET, IS_LOOP, 
                                 DURATION_TIME_CODE, DEBUG):
        
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/liveScheduleEvent"

    SCHEDULE_EVENT_INFO = _get_asset_schedule_event(self, AUTH_TOKEN, URL, CHANNEL_ID, 
                                                    ID, DEBUG)

    BODY = {
        "type": {
            "id": _EVENT_TYPES["videoAsset"],
            "description": "Video Asset"
        }
    }

    BODY['id'] = ID if ID and ID != SCHEDULE_EVENT_INFO['id'] else SCHEDULE_EVENT_INFO['id']
    BODY['isLoop'] = IS_LOOP if IS_LOOP and IS_LOOP != SCHEDULE_EVENT_INFO['isLoop'] else SCHEDULE_EVENT_INFO['isLoop']
    BODY['channelId'] = CHANNEL_ID if CHANNEL_ID and CHANNEL_ID != SCHEDULE_EVENT_INFO['channelId'] else SCHEDULE_EVENT_INFO['channelId']
    BODY['durationTimeCode'] = DURATION_TIME_CODE if DURATION_TIME_CODE and DURATION_TIME_CODE != SCHEDULE_EVENT_INFO['durationTimeCode'] else SCHEDULE_EVENT_INFO['durationTimeCode']
    BODY['asset'] = ASSET if ASSET and ASSET != SCHEDULE_EVENT_INFO['asset'] else SCHEDULE_EVENT_INFO['asset']
    
    return _send_request(self, AUTH_TOKEN, "Update Asset Schedule Event", API_URL, "PUT", None, BODY, DEBUG)