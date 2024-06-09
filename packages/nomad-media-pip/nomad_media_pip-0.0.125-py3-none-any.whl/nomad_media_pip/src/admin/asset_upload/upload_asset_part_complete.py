from nomad_media_pip.src.helpers.send_request import _send_request

import json, requests, time
MAX_RETRIES = 2

def _upload_asset_part_complete(self, AUTH_TOKEN, URL, PART_ID, ETAG, DEBUG):

    API_URL = f"{URL}/api/asset/upload/part/" + PART_ID + "/complete"

    # Build the payload BODY
    BODY = {
        "etag": ETAG
    }

    return _send_request(self, AUTH_TOKEN, "Upload Asset Part Complete", API_URL, "POST", None, BODY, DEBUG)

