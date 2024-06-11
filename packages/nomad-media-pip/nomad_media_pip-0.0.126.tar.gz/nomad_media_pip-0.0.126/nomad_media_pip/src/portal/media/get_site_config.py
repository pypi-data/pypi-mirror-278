from nomad_media_pip.src.helpers.send_request import _send_request

def _get_site_config(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/media/config/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get Site Config", API_URL, "GET", None, None, DEBUG)