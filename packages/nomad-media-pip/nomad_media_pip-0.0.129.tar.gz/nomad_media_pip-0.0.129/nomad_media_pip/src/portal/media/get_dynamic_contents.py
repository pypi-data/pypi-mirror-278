from nomad_media_pip.src.helpers.send_request import _send_request

def _get_dynamic_contents(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/api/media/content"

    return _send_request(self, AUTH_TOKEN, "Get Dynamic Contents", API_URL, "GET", None, None, DEBUG)