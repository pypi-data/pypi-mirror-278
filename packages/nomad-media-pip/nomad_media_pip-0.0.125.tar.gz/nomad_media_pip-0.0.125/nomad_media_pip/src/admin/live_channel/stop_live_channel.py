from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_channel.live_channel_statuses import _LIVE_CHANNEL_STATUSES
from nomad_media_pip.src.admin.live_channel.wait_for_live_channel_status import _wait_for_live_channel_status

import json, requests, time

MAX_RETRIES = 2

def _stop_live_channel(self, AUTH_TOKEN, URL, CHANNEL_ID, WAIT_FOR_STOP, DEBUG):
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/stop"
    
    _send_request(self, AUTH_TOKEN, "Stop Live Channel", API_URL, "POST", None, None, DEBUG)
    if WAIT_FOR_STOP: _wait_for_live_channel_status(self, AUTH_TOKEN, URL, CHANNEL_ID, _LIVE_CHANNEL_STATUSES["Idle"], 120, 2, DEBUG)

