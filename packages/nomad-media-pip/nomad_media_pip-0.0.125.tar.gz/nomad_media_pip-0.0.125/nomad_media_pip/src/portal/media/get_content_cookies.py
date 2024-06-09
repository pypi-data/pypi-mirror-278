from nomad_media_pip.src.helpers.send_request import _send_request

def _get_content_cookies(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/media/set-cookies/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get Content Cookies", API_URL, "GET", None, None, DEBUG)