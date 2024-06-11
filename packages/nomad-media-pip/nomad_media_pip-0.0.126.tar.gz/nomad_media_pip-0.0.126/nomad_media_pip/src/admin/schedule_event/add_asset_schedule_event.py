from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule_event.event_types import _EVENT_TYPES

def _add_asset_schedule_event(self, AUTH_TOKEN, URL, CHANNEL_ID, ASSET, IS_LOOP,
                              DURATION_TIME_CODE, PREVIOUS_ID, DEBUG):
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/liveScheduleEvent" 
    
    # Build the payload BODY
    BODY = {
        "isLoop": IS_LOOP,
        "channelId": CHANNEL_ID,
        "durationTimeCode": DURATION_TIME_CODE,
        "previousId": PREVIOUS_ID,
        "type": {
            "id": _EVENT_TYPES["videoAsset"],
            "description": "Video-Asset"
        },
        "asset": ASSET,
    }

    return _send_request(self, AUTH_TOKEN, "Add Asset Schedule Event", API_URL, "POST\nBODY: {json.dumps(BODY", None, BODY, DEBUG)