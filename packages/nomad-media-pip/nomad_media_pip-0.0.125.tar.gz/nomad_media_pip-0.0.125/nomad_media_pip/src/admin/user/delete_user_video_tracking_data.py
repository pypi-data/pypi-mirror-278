from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_user_video_tracking_data(self, AUTH_TOKEN, URL, ASSET_ID, CONTENT_ID,
                                     VIDEO_TRACKING_ATTRIBUTE, USER_ID, ID, IS_FIRST_QUARTILE,
                                     IS_MIDPOINT, IS_THIRD_QUARTILE, IS_COMPLETE, IS_HIDDEN,
                                     IS_LIVE_STREAM, MAX_SECONDS, LAST_SECOND, TOTAL_SECONDS,
                                     LAST_BEACON_DATE, KEY_NAME, DEBUG):
    
    API_URL = f"{URL}/api/admin/user/userVideoTracking/delete"
    
    BODY = {
        "assetId": ASSET_ID,
        "contentId": CONTENT_ID,
        "videoTrackingAttribute": VIDEO_TRACKING_ATTRIBUTE,
        "userId": USER_ID,
        "id": ID,
        "isFirstQuartile": IS_FIRST_QUARTILE,
        "isMidpoint": IS_MIDPOINT,
        "isThirdQuartile": IS_THIRD_QUARTILE,
        "isComplete": IS_COMPLETE,
        "isHidden": IS_HIDDEN,
        "isLiveStream": IS_LIVE_STREAM,
        "maxSeconds": MAX_SECONDS,
        "lastSecond": LAST_SECOND,
        "totalSeconds": TOTAL_SECONDS,
        "lastBeaconDate": LAST_BEACON_DATE,
        "keyName": KEY_NAME
    }

    return _send_request(self, AUTH_TOKEN, "Delete User Video Tracking Data", API_URL, "POST", None, BODY, DEBUG)