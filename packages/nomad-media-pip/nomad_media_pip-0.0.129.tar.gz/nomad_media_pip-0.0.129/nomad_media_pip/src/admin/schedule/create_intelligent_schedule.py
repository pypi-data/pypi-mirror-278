from nomad_media_pip.src.helpers.send_request import _send_request

def _create_intelligent_schedule(self, AUTH_TOKEN, URL, DEFAULT_VIDEO_ASSET, NAME, THUMBNAIL_ASSET, 
                                 TIME_ZONE_ID, DEBUG):
    
    API_URL = f"{URL}/api/admin/schedule"
    
    BODY = {
        "defaultVideoAsset": DEFAULT_VIDEO_ASSET,
        "name": NAME,
        "scheduleType": "3",
        "thumbnailAsset": THUMBNAIL_ASSET,
        "timeZoneId": TIME_ZONE_ID
    }

    return _send_request(self, AUTH_TOKEN, "Create Intelligent Schedule", API_URL, "POST", None, BODY, DEBUG)