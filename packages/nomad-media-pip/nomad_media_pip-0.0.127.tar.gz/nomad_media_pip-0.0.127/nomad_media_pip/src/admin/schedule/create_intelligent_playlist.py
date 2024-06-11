from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.delete_intelligent_playlist import _delete_intelligent_playlist

def _create_intelligent_playlist(self, AUTH_TOKEN, URL, COLLECTIONS, END_SEARCH_DATE, 
                                 END_SEARCH_DURATION_IN_MINUTES, NAME, RELATED_CONTENT, 
                                 SEARCH_DATE, SEARCH_DURATION_IN_MINUTES, SEARCH_FILTER_TYPE, 
                                 TAGS, THUMBNAIL_ASSET, DEBUG):
    
    SCHEDULE_API_URL = f"{URL}/api/admin/schedule"

    SCHEUDLE_BODY = {
        "name": NAME,
        "scheduleType": "4",
        "thumbnailAsset": THUMBNAIL_ASSET
    }

    SCHEDULE_INFO = _send_request(self, AUTH_TOKEN, "Creating Intelligent Playlist", SCHEDULE_API_URL, "POST", None, SCHEUDLE_BODY, DEBUG)

    ITEM_API_URL = f"{SCHEDULE_API_URL}/{SCHEDULE_INFO['id']}/item"

    ITEM_BODY = {
        "collections": COLLECTIONS,
        "endSearchDate": END_SEARCH_DATE,
        "endSearchDurationInMinutes": END_SEARCH_DURATION_IN_MINUTES,
        "name": NAME,
        "relatedContent": RELATED_CONTENT,
        "searchDate": SEARCH_DATE,
        "searchDurationInMinutes": SEARCH_DURATION_IN_MINUTES,
        "searchFilterType": SEARCH_FILTER_TYPE,
        "tags": TAGS,
        "thumbnailAsset": THUMBNAIL_ASSET
    }

    ITEM_INFO = _send_request(self, AUTH_TOKEN, "Creating Intelligent Playlist", ITEM_API_URL, "POST", None, ITEM_BODY, DEBUG)

    for param in SCHEDULE_INFO:
        ITEM_INFO[param] = SCHEDULE_INFO[param]
        
    return ITEM_INFO