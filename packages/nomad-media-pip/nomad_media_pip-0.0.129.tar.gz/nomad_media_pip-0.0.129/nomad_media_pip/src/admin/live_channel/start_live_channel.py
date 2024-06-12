from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_channel.live_channel_statuses import _LIVE_CHANNEL_STATUSES
from nomad_media_pip.src.admin.live_channel.wait_for_live_channel_status import _wait_for_live_channel_status

def _start_live_channel(self, AUTH_TOKEN, URL, CHANNEL_ID, WAIT_FOR_START, DEBUG):
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/start"
    
    _send_request(self, AUTH_TOKEN, "Start Live Channel", API_URL, "POST", None, None, DEBUG)
    if WAIT_FOR_START: _wait_for_live_channel_status(self, AUTH_TOKEN, URL, CHANNEL_ID, _LIVE_CHANNEL_STATUSES["Running"], 1200, 20, DEBUG)

