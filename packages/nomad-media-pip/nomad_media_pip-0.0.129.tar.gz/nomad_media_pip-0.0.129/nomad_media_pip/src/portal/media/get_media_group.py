from nomad_media_pip.src.helpers.send_request import _send_request

def _get_media_group(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/media/group/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get Media Group", API_URL, "GET", None, None, DEBUG)