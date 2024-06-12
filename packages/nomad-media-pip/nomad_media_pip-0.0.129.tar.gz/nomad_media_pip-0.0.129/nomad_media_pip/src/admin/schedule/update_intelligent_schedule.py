from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_intelligent_schedule import _get_intelligent_schedule

def _update_intelligent_schedule(self, AUTH_TOKEN, URL, ID, DEFAULT_VIDEO_ASSET, NAME, THUMBNAIL_ASSET, 
                               TIME_ZONE_ID, DEBUG):
    
    API_URL = f"{URL}/api/admin/schedule/{ID}"
    
    SCHEDULE = _get_intelligent_schedule(self, AUTH_TOKEN, URL, ID, DEBUG)
       
    BODY = {
        "defaultVideoAsset": DEFAULT_VIDEO_ASSET or SCHEDULE.get("defaultVideoAsset"),
        "name": NAME or SCHEDULE.get("name"),
        "scheduleType": "3",
        "thumbnailAsset": THUMBNAIL_ASSET or SCHEDULE.get("thumbnailAsset"),
        "timeZoneId": TIME_ZONE_ID or SCHEDULE.get("timeZoneId"),
        "id": ID,
    }

    return _send_request(self, AUTH_TOKEN, "Update Intelligent Schedule", API_URL, "PUT", None, BODY, DEBUG)