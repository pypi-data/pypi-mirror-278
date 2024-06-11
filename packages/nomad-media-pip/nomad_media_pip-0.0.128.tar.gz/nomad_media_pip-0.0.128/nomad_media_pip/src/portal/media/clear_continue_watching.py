from nomad_media_pip.src.helpers.send_request import _send_request

def _clear_continue_watching(self, AUTH_TOKEN, URL, USER_ID, ASSET_ID, DEBUG):

    API_URL = f"{URL}/api/media/clear-watching"

    PARAMS = {
        "userId": USER_ID,
        "assetId": ASSET_ID
    }

    return _send_request(self, AUTH_TOKEN, "Clear Continue Watching", API_URL, "POST", PARAMS, None, DEBUG)