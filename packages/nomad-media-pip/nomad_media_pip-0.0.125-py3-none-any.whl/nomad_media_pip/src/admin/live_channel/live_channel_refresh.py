from nomad_media_pip.src.helpers.send_request import _send_request

def _live_channel_refresh(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/api/liveChannel/refresh"

    return _send_request(self, AUTH_TOKEN, "Live Channel Refresh", API_URL, "POST", None, None, DEBUG)