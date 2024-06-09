from nomad_media_pip.src.helpers.send_request import _send_request

def _get_my_content(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/api/media/my-content"

    return _send_request(self, AUTH_TOKEN, "Get My Content", API_URL, "GET", None, None, DEBUG)