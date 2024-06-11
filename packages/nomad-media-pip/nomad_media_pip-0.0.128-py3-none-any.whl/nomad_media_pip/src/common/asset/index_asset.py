from nomad_media_pip.src.helpers.send_request import _send_request

def _index_asset(self, AUTH_TOKEN, URL, ASSET_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/index"

    return _send_request(self, AUTH_TOKEN, "Index asset", API_URL, "POST", None, None, DEBUG)