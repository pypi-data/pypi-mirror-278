from nomad_media_pip.src.helpers.send_request import _send_request

def _get_asset_ad_breaks(self, AUTH_TOKEN, URL, ASSET_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/adbreak"

    return _send_request(self, AUTH_TOKEN, "Get asset ad breaks", API_URL, "GET", None, None, DEBUG)