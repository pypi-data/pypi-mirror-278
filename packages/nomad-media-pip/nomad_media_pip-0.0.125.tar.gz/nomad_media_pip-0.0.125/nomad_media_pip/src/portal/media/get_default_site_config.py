from nomad_media_pip.src.helpers.send_request import _send_request

def _get_default_site_config(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/api/media/config"

    return _send_request(self, AUTH_TOKEN, "Get Default Site Config", API_URL, "GET", None, None, DEBUG)