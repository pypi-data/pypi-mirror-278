from nomad_media_pip.src.helpers.send_request import _send_request

def _restore_asset(self, AUTH_TOKEN, URL, ASSET_ID, API_TYPE, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/restore" if API_TYPE == "admin" else f"{URL}/api/asset/{ASSET_ID}/restore"

    return _send_request(self, AUTH_TOKEN, "Restore asset", API_URL, "POST", None, None, DEBUG)