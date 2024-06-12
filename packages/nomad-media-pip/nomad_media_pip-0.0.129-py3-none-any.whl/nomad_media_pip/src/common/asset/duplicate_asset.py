from nomad_media_pip.src.helpers.send_request import _send_request

def _duplicate_asset(self, AUTH_TOKEN, URL, ASSET_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/duplicate"

    return _send_request(self, AUTH_TOKEN, "Duplicate asset", API_URL, "POST", None, None, DEBUG)