from nomad_media_pip.src.helpers.send_request import _send_request

def _create_schedule_item_live_channel(self, AUTH_TOKEN, URL, SCHEUDLE_ID, DAYS, DURATION_TIME_CODE,
                                       END_TIME_CODE, LIVE_CHANNEL, PREVIOUS_ITEM, TIME_CODE, 
                                       DEBUG):
    
    API_URL = f"{URL}/api/admin/schedule/{SCHEUDLE_ID}/item"
       
    BODY = {
        "days": DAYS,
        "durationTimeCode": DURATION_TIME_CODE,
        "endTimeCode": END_TIME_CODE,
        "liveChannel": LIVE_CHANNEL,
        "previousItem": PREVIOUS_ITEM,
        "scheduleItemType": "1",
        "sourceType": "4",
        "timeCode": TIME_CODE
    }
    
    return _send_request(self, AUTH_TOKEN, "Create Schedule Item Live Channel", API_URL, "POST", None, BODY, DEBUG)