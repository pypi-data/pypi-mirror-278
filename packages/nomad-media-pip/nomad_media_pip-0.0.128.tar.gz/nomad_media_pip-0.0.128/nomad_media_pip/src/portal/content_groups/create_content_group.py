from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_content_group(self, AUTH_TOKEN, URL, CONTENT_GROUP_NAME, DEBUG):
    API_URL = f"{URL}/api/contentGroup"

    BODY = {
        "Name": CONTENT_GROUP_NAME
    }

    return _send_request(self, AUTH_TOKEN, "Create content groups", API_URL, "POST", None, BODY, DEBUG)
    