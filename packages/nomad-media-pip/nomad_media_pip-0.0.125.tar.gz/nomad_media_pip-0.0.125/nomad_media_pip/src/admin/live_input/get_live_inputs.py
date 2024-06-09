from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_inputs(self, AUTH_TOKEN, URL, DEBUG):
    API_URL = f"{URL}/api/liveInput"

    return _send_request(self, AUTH_TOKEN, "Get Live Inputs", API_URL, "GET", None, None, DEBUG)