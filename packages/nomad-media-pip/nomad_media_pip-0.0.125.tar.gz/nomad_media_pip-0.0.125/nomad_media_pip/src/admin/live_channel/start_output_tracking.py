from nomad_media_pip.src.helpers.send_request import _send_request

def _start_output_tracking(self, AUTH_TOKEN, URL, LIVE_CHANNEL_ID, DEBUG):

    API_URL = f"{URL}/api/liveChannel/{LIVE_CHANNEL_ID}/startOutputTracking"

    return _send_request(self, AUTH_TOKEN, "Start Output Tracking", API_URL, "POST", None, None, DEBUG) 