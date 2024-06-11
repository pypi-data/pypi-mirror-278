from nomad_media_pip.src.helpers.send_request import _send_request

def _get_asset_screenshot_details(self, AUTH_TOKEN, URL, ASSET_ID, SEGMENT_ID, SCREENSHOT_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/{SEGMENT_ID}/{SCREENSHOT_ID}/detail"

    return _send_request(self, AUTH_TOKEN, "Get asset screenshot details", API_URL, "GET", None, None, DEBUG)