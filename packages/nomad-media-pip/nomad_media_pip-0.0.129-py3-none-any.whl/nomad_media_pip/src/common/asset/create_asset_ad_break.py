from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_asset_ad_break(self, AUTH_TOKEN, URL, ASSET_ID, TIME_CODE, TAGS, LABELS, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/adbreak"

    BODY = {
        "id": ASSET_ID,
        "timecode": TIME_CODE
    }

    if TAGS:
        BODY["tags"] = TAGS

    if LABELS:
        BODY["labels"] = LABELS

    return _send_request(self, AUTH_TOKEN, "Create ad break", API_URL, "POST", None, BODY, DEBUG)
    