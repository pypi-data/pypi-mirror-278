from nomad_media_pip.src.helpers.send_request import _send_request

def _records_asset_tracking_beacon(self, AUTH_TOKEN, URL, ASSET_ID, TRACKING_EVENT, LIVE_CHANNEL_ID,
                                  CONTENT_ID, SECOND, DEBUG):
    
    API_URL = f"{URL}/api/asset/tracking"

    PARAMS = {
        "trackingEvent": TRACKING_EVENT,
        "assetId": ASSET_ID,
        "liveChannelId": LIVE_CHANNEL_ID,
        "contentId": CONTENT_ID,
        "second": SECOND
    }

    return _send_request(self, AUTH_TOKEN, "Record asset tracking beacon", API_URL, "GET", PARAMS, None, DEBUG)