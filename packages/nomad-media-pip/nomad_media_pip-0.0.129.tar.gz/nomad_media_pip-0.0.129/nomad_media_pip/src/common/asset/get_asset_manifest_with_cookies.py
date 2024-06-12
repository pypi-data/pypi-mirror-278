from nomad_media_pip.src.helpers.send_request import _send_request

def _get_asset_manifest_with_cookies(self, AUTH_TOKEN, URL, ASSET_ID, COOKIE_ID, API_TYPE, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/set-cookies/{COOKIE_ID}" if API_TYPE == "admin" else f"{URL}/api/asset/{ASSET_ID}/set-cookies/{COOKIE_ID}"

    return _send_request(self, AUTH_TOKEN, "Get asset manifest with cookies", API_URL, "GET", None, None, DEBUG)