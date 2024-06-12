from nomad_media_pip.src.helpers.send_request import _send_request

def _get_asset_metadata_summary(self, AUTH_TOKEN, URL, ASSET_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/metadata-summary"

    return _send_request(self, AUTH_TOKEN, "Get asset metadata summary", API_URL, "GET", None, None, DEBUG)