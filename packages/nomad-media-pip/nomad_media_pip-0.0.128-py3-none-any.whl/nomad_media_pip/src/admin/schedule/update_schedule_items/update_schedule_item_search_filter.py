from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_schedule_item import _get_schedule_item

def _update_schedule_item_search_filter(self, AUTH_TOKEN, URL, ID, ITEM_ID, COLLECTIONS, DAYS, 
                                        DURATION_TIME_CODE, END_SEARCH_DATE, 
                                        END_SEARCH_DURATION_IN_MINUTES, END_TIME_CODE, 
                                        RELATED_CONTENT, SEARCH_DATE, SEARCH_DURATION_IN_MINUTES, 
                                        SEARCH_FILTER_TYPE, TAGS, TIME_CODE, DEBUG):

    API_URL = f"{URL}/api/admin/schedule/{ID}/item/{ITEM_ID}"

    SCHEDULE_ITEM = _get_schedule_item(self, AUTH_TOKEN, URL, ID, ITEM_ID, DEBUG)
    
    BODY = {
        "collections": COLLECTIONS or SCHEDULE_ITEM.get("collections"),
        "days": DAYS or SCHEDULE_ITEM.get("days"),
        "durationTimeCode": DURATION_TIME_CODE or SCHEDULE_ITEM.get("durationTimeCode"),
        "endSearchDate": END_SEARCH_DATE or SCHEDULE_ITEM.get("endSearchDate"),
        "endSearchDurationInMinutes": END_SEARCH_DURATION_IN_MINUTES or SCHEDULE_ITEM.get("endSearchDurationInMinutes"),
        "endTimeCode": END_TIME_CODE or SCHEDULE_ITEM.get("endTimeCode"),
        "relatedContent": RELATED_CONTENT or SCHEDULE_ITEM.get("relatedContent"),
        "scheduleItemType": "1",
        "searchDate": SEARCH_DATE or SCHEDULE_ITEM.get("searchDate"),
        "searchDurationInMinutes": SEARCH_DURATION_IN_MINUTES or SCHEDULE_ITEM.get("searchDurationInMinutes"),
        "searchFilterType": SEARCH_FILTER_TYPE or SCHEDULE_ITEM.get("searchFilterType"),
        "sourceType": "2",
        "tags": TAGS or SCHEDULE_ITEM.get("tags"),
        "timeCode": TIME_CODE or SCHEDULE_ITEM.get("timeCode")
    }

    return _send_request(self, AUTH_TOKEN, "Update Schedule Item Search Filter", API_URL, "PUT", None, BODY, DEBUG)