from nomad_media_pip.src.helpers.send_request import _send_request

def _get_media_builder_items(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/mediaBuilder/{ID}/items"

    return _send_request(self, AUTH_TOKEN, "Get Media Builder Items", API_URL, "GET", None, None, DEBUG)