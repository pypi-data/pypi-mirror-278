from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_schedule_item import _get_schedule_item

def _update_schedule_item_live_channel(self, AUTH_TOKEN, URL, ID, ITEM_ID, DAYS, DURATION_TIME_CODE, 
                                       END_TIME_CODE, LIVE_CHANNEL, TIME_CODE, DEBUG):

    SCHEDULE_ITEM = _get_schedule_item(self, AUTH_TOKEN, URL, ID, ITEM_ID, DEBUG)

    API_URL = f"{URL}/api/admin/schedule/{ID}/item/{ITEM_ID}"
    
    BODY = {
        "days": DAYS or SCHEDULE_ITEM.get("days"),
        "durationTimeCode": DURATION_TIME_CODE or SCHEDULE_ITEM.get("durationTimeCode"),
        "endTimeCode": END_TIME_CODE or SCHEDULE_ITEM.get("endTimeCode"),
        "liveChannel": LIVE_CHANNEL or SCHEDULE_ITEM.get("liveChannel"),
        "scheduleItemType": "1",
        "sourceType": "4",
        "timeCode": TIME_CODE or SCHEDULE_ITEM.get("timeCode")
    }

    return _send_request(self, AUTH_TOKEN, "Update Schedule Item Live Channel", API_URL, "PUT", None, BODY, DEBUG)