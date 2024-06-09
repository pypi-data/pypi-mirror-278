from nomad_media_pip.src.helpers.send_request import _send_request

def _archive_asset(self, AUTH_TOKEN, URL, ASSET_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/archive"

    return _send_request(self, AUTH_TOKEN, "Archive asset", API_URL, "POST", None, None, DEBUG)