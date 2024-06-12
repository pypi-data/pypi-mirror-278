from nomad_media_pip.src.helpers.send_request import _send_request

def _get_annotations(self, AUTH_TOKEN, URL, ASSET_ID, DEBUG):

    API_URL = f"{URL}/api/asset/{ASSET_ID}/annotation"

    return _send_request(self, AUTH_TOKEN, "Get asset annotations", API_URL, "GET", None, None, DEBUG)