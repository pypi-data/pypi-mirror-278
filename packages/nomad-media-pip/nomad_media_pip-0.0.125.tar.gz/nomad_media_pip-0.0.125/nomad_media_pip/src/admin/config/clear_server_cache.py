from nomad_media_pip.src.helpers.send_request import _send_request

def _clear_server_cache(self, AUTH_TOKEN, URL, DEBUG):
    API_URL = f"{URL}/api/config/clearServerCache"

    return _send_request(self, AUTH_TOKEN, "Clear server cache", API_URL, "POST", None, None, DEBUG)