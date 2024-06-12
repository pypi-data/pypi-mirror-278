from nomad_media_pip.src.helpers.send_request import _send_request

def _get_media_builders(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/api/mediaBuilder"

    return _send_request(self, AUTH_TOKEN, "Get Media Builders", API_URL, "GET", None, None, DEBUG)