from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_annotation(self, AUTH_TOKEN, URL, ASSET_ID, START_TIME_CODE, END_TIME_CODE, TITLE,
                       SUMMARY, DESCRIPTION, DEBUG):
    
    API_URL = f"{URL}/api/asset/{ASSET_ID}/annotation"

    BODY = {
        "startTimecode": START_TIME_CODE,
        "endTimecode": END_TIME_CODE,
        "properties": {
            "title": TITLE,
            "description": DESCRIPTION,
            "summary": SUMMARY
        }
    }

    return _send_request(self, AUTH_TOKEN, "Create annotation", API_URL, "POST", None, BODY, DEBUG)
    