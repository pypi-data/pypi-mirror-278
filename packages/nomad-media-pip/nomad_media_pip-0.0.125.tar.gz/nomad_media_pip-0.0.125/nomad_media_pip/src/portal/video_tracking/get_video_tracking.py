from nomad_media_pip.src.helpers.send_request import _send_request

def _get_video_tracking(self, AUTH_TOKEN, URL, ASSET_ID, TRACKING_EVENT, SECOND, DEBUG) :
    API_URL = f"{URL}/api/asset/tracking?assetId={ASSET_ID}"

    PARAMS = {
        "event": TRACKING_EVENT,
        "second": SECOND
    }
        
    return _send_request(self, AUTH_TOKEN, "Get video tracking service", API_URL, "GET", PARAMS, None, DEBUG)