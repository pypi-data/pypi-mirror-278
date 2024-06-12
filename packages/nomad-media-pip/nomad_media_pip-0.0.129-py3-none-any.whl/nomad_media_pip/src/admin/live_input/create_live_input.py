from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.helpers.slugify import _slugify
from nomad_media_pip.src.admin.live_input.live_input_types import _LIVE_INPUT_TYPES
from nomad_media_pip.src.admin.live_input.live_input_statuses import _LIVE_INPUT_STATUSES
from nomad_media_pip.src.admin.live_input.wait_for_live_input_status import _wait_for_live_input_status

def _create_live_input(self, AUTH_TOKEN, URL, NAME, SOURCE, TYPE, IS_STANDARD, VIDEO_ASSET_ID, 
                       DESTINATIONS, SOURCES, DEBUG):
    API_URL = f"{URL}/api/liveInput"

    BODY = {
        "name": NAME,
        "internalName": _slugify(NAME),
        "type": { 
            "id": _LIVE_INPUT_TYPES[TYPE],
            "description": TYPE
        }
    }

    # Set the appropriate fields based on the type
    if (TYPE == "RTMP_PUSH"):
        if SOURCE: BODY["sourceCidr"] = SOURCE
    elif (TYPE == "RTMP_PULL" or TYPE == "RTP_PUSH" or TYPE == "URL_PULL"):
        if SOURCE: BODY["sources"] = [{ "url": SOURCE }]

    if IS_STANDARD: BODY["isStandard"] = IS_STANDARD
    if VIDEO_ASSET_ID: BODY["videoAsset"] = { "id": VIDEO_ASSET_ID }
    if DESTINATIONS: BODY["destinations"] = DESTINATIONS
    if SOURCES: BODY["sources"] = SOURCES

    INFO = _send_request(self, AUTH_TOKEN, "Create Live Input", API_URL, "POST", None, BODY, DEBUG)
    _wait_for_live_input_status(self, AUTH_TOKEN, URL, INFO["id"], _LIVE_INPUT_STATUSES["Detached"], 15, 1)
    return INFO

