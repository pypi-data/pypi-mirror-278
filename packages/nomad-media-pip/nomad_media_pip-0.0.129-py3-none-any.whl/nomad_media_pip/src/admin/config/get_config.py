from nomad_media_pip.src.helpers.send_request import _send_request

def _get_config(self, AUTH_TOKEN, URL, CONFIG_TYPE, DEBUG):
    API_URL = f"{URL}/api/config?configType={CONFIG_TYPE}"

    return _send_request(self, AUTH_TOKEN, "Get Config", API_URL, "GET", None, None, DEBUG)