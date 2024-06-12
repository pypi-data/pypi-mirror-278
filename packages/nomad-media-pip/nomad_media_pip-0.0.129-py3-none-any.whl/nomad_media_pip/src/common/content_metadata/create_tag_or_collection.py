from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_tag_or_collection(self, AUTH_TOKEN, URL, TYPE, TAG_NAME, DEBUG):
    
    API_URL = f"{URL}/api/admin/{TYPE}"

    BODY = {
        "name": TAG_NAME
    }
    
    return _send_request(self, AUTH_TOKEN, "Create Tag or Collection", API_URL, "POST", None, BODY, DEBUG)
    