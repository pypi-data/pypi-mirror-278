from nomad_media_pip.src.helpers.send_request import _send_request

def _create_schedule_item_asset(self, AUTH_TOKEN, URL, SCHEUDLE_ID, ASSET, DAYS, DURATION_TIME_CODE,
                                END_TIME_CODE, PREVIOUS_ITEM, TIME_CODE, DEBUG):
        
    API_URL = f"{URL}/api/admin/schedule/{SCHEUDLE_ID}/item"
       
    BODY = {
        "asset": ASSET,
        "days": DAYS,
        "durationTimeCode": DURATION_TIME_CODE,
        "endTimeCode": END_TIME_CODE,
        "previousItem": PREVIOUS_ITEM,
        "scheduleItemType": "1",
        "sourceType": "3",
        "timeCode": TIME_CODE
    }
    
    return _send_request(self, AUTH_TOKEN, "Create Schedule Item Asset", API_URL, "POST", None, BODY, DEBUG)