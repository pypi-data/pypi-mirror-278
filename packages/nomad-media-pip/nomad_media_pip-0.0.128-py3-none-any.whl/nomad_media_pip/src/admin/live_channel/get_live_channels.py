from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_channels(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/api/liveChannel"
    return _send_request(self, AUTH_TOKEN, "Get Live Channels", API_URL, "GET", None, None, DEBUG)