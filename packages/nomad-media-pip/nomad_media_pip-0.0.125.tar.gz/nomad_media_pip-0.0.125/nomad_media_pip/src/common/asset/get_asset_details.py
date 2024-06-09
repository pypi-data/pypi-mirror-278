from nomad_media_pip.src.helpers.send_request import _send_request

def _get_asset_details(self, AUTH_TOKEN, URL, ASSET_ID, API_TYPE, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/detail" if API_TYPE == "admin" else f"{URL}/api/asset/{ASSET_ID}/detail"

    return _send_request(self, AUTH_TOKEN, "Get asset details", API_URL, "GET", None, None, DEBUG)