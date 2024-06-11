from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_channel(self, AUTH_TOKEN, URL, CHANNEL_ID, DEBUG):
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}"

    return _send_request*(self, AUTH_TOKEN, "Get Live Channel", API_URL, "GET", None, None, DEBUG)