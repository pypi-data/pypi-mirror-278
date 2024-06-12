from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_screenshot_at_timecode(self, AUTH_TOKEN, URL, ASSET_ID, TIME_CODE, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/screenshot"

    BODY = {
        "timecode": TIME_CODE
    }

    return _send_request(self, AUTH_TOKEN, "Create screenshot at timecode", API_URL, "POST", None, BODY, DEBUG)
    