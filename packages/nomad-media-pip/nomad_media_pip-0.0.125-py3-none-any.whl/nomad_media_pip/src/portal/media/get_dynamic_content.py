from nomad_media_pip.src.helpers.send_request import _send_request

def _get_dynamic_content(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/media/content/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get Dynamic Content", API_URL, "GET", None, None, DEBUG)