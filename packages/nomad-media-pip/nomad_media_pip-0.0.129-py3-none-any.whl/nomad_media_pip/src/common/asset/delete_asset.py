from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_asset(self, AUTH_TOKEN, URL, ASSET_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}"

    return _send_request(self, AUTH_TOKEN, "Delete asset", API_URL, "DELETE", None, None, DEBUG)