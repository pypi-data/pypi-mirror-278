from nomad_media_pip.src.helpers.send_request import _send_request

def _create_schedule_item_playlist_schedule(self, AUTH_TOKEN, URL, SCHEUDLE_ID, DAYS, 
                                            DURATION_TIME_CODE, END_TIME_CODE, 
                                            PLAYLIST_SCHEDULE, PREVIOUS_ITEM, TIME_CODE, 
                                            DEBUG):
        
    API_URL = f"{URL}/api/admin/schedule/{SCHEUDLE_ID}/item"
       
    BODY = {
        "days": DAYS,
        "durationTimeCode": DURATION_TIME_CODE,
        "endTimeCode": END_TIME_CODE,
        "playlistSchedule": PLAYLIST_SCHEDULE,
        "previousItem": PREVIOUS_ITEM,
        "scheduleItemType": "2",
        "sourceType": "1",
        "timeCode": TIME_CODE
    }
    
    return _send_request(self, AUTH_TOKEN, "Create Schedule Item Playlist Schedule", API_URL, "POST", None, BODY, DEBUG)