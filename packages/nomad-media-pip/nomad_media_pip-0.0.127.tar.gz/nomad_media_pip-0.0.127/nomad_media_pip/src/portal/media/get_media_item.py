from nomad_media_pip.src.helpers.send_request import _send_request

def _get_media_item(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/media/item/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get Media Item", API_URL, "GET", None, None, DEBUG)