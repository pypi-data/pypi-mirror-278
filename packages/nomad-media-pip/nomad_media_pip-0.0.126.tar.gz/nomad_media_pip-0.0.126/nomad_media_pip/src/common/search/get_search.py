from nomad_media_pip.src.helpers.send_request import _send_request

def _get_search(self, AUTH_TOKEN, URL, ID, API_TYPE, DEBUG):
    API_URL = f"{URL}/api/{API_TYPE}/search/{ID}"

    return _send_request(self, AUTH_TOKEN, "Searching", API_URL, "GET", None, None, DEBUG)