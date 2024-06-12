from nomad_media_pip.src.helpers.send_request import _send_request

def _add_tag_or_collection(self, AUTH_TOKEN, URL, TYPE, CONTENT_ID, CONTENT_DEFINITION, NAME, 
                           TAG_ID, CREATE_NEW, API_TYPE, DEBUG):

    API_URL = f"{URL}/api/admin/{TYPE}/content" if API_TYPE == "admin" else f"{URL}/api/content/{TYPE}"
        
    BODY = {
        "items": [
            {
                "contentDefinition": CONTENT_DEFINITION,
                "contentId": CONTENT_ID,
                "name": NAME,
                "createNew": CREATE_NEW,
                f"{TYPE}Id": TAG_ID
            }
        ]
    }

    return _send_request(self, AUTH_TOKEN, f"Add {TYPE}", API_URL, "POST", None, BODY, DEBUG)