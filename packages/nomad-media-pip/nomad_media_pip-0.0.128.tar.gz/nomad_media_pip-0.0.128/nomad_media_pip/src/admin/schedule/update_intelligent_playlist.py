from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_intelligent_playlist import _get_intelligent_playlist
from nomad_media_pip.src.admin.schedule.get_schedule_items import _get_schedule_items

def _update_intelligent_playlist(self, AUTH_TOKEN, URL, ID, COLLECTIONS, END_SEARCH_DATE, 
                                 END_SEARCH_DURATION_IN_MINUTES, NAME, RELATED_CONTENT, 
                                 SEARCH_DATE, SEARCH_DURATION_IN_MINUTES, SEARCH_FILTER_TYPE, 
                                 TAGS, THUMBNAIL_ASSET, DEBUG):

    SCHEDULE_API_URL = f"{URL}/api/admin/schedule/{ID}"

    PLAYLIST_INFO = _get_intelligent_playlist(self, AUTH_TOKEN, URL, ID, DEBUG)

    SCHEDULE_BODY = {
        "name": NAME or PLAYLIST_INFO.get("name"),
        "scheduleType": "4",
        "thumbnailAsset": THUMBNAIL_ASSET or PLAYLIST_INFO.get("thumbnailAsset"),
        "scheduleStatus": PLAYLIST_INFO.get("scheduleStatus"),
        "status": PLAYLIST_INFO.get("status")
    }

    SCHEDULE_INFO = _send_request(self, AUTH_TOKEN, "Update Intelligent Playlist", SCHEDULE_API_URL, "PUT", SCHEDULE_BODY, None, DEBUG)

    ITEM_INFO = _get_schedule_items(self, AUTH_TOKEN, URL, ID, DEBUG)
    ITEM = ITEM_INFO[0]

    ITEM_API_URL = f"{SCHEDULE_API_URL}/item/{ITEM['id']}"

    ITEM_BODY = {
        'id': ITEM['id'],
        'collections': COLLECTIONS if COLLECTIONS != [] else ITEM.get("collections"),
        'endSearchDate': END_SEARCH_DATE if END_SEARCH_DATE else ITEM.get("endSearchDate"),
        'endSearchDurationInMinutes': END_SEARCH_DURATION_IN_MINUTES if END_SEARCH_DURATION_IN_MINUTES else ITEM.get("endSearchDurationInMinutes"),
        'relatedContent': RELATED_CONTENT if RELATED_CONTENT != [] else ITEM.get("relatedContent"),
        'scheduleItemType': "2",
        'searchDate': SEARCH_DATE if SEARCH_DATE else ITEM.get("searchDate"),
        'searchDurationInMinutes': SEARCH_DURATION_IN_MINUTES if SEARCH_DURATION_IN_MINUTES else ITEM.get("searchDurationInMinutes"),
        'searchFilterType': SEARCH_FILTER_TYPE if SEARCH_FILTER_TYPE else ITEM.get("searchFilterType"),
        'sourceType': "2",
        'tags': TAGS if TAGS != [] else ITEM.get("tags")
    }

    return _send_request(self, AUTH_TOKEN, "Update Intelligent Playlist", ITEM_API_URL, "PUT", ITEM_BODY, None, DEBUG)