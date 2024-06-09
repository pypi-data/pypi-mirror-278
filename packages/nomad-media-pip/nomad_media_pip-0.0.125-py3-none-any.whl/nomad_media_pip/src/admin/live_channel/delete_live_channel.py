from nomad_media_pip.src.admin.live_channel.get_live_channel_inputs_ids import _get_live_channel_inputs_ids
from nomad_media_pip.src.admin.live_input.delete_live_input import _delete_live_input
from nomad_media_pip.src.helpers.send_request import _send_request

import requests, json, time
MAX_RETRIES = 2

def _delete_live_channel(self, AUTH_TOKEN, URL, CHANNEL_ID, DELETE_INPUTS, DEBUG):
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}"

    # If delete Live Inputs then get their IDs
    INPUT_IDS = None
    if (DELETE_INPUTS == True):
        INPUT_IDS = _get_live_channel_inputs_ids(self, AUTH_TOKEN, URL, CHANNEL_ID, DEBUG)

    if (DELETE_INPUTS and INPUT_IDS and len(INPUT_IDS) > 0):
        print("Deleting Channel Inputs...")
        # Loop deleted Live Channel Live Inputs
        for ID in INPUT_IDS:
            # Delete Live Input
            _delete_live_input(self, AUTH_TOKEN, URL, ID, DEBUG)

    _send_request(self, AUTH_TOKEN, "Delete Live Channel", API_URL, "DELETE", None, None, DEBUG)