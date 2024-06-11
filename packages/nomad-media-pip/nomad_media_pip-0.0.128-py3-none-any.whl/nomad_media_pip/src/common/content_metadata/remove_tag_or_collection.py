from nomad_media_pip.src.helpers.send_request import _send_request 

def _remove_tag_or_collection(self, AUTH_TOKEN, URL, TYPE, CONTENT_ID, CONTENT_DEFINITION,
                              TAG_ID, API_TYPE, DEBUG):

    API_URL = f"{URL}/api/admin/{TYPE}/content/delete" if API_TYPE == "admin" else f"{URL}/api/content/{TYPE}/delete"

    BODY = {
        "items": [
            {
                "contentDefinition": CONTENT_DEFINITION,
                "contentId": CONTENT_ID,
                f"{TYPE}Id": TAG_ID
            }
        ]
    }

    return _send_request(self, AUTH_TOKEN, "delete tag or colleciton", API_URL, "POST,", None, BODY, DEBUG)
    