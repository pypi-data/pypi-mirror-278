from nomad_media_pip.src.helpers.send_request import _send_request

def _get_media_builder(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/mediaBuilder/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get Media Builder", API_URL, "GET", None, None, DEBUG)