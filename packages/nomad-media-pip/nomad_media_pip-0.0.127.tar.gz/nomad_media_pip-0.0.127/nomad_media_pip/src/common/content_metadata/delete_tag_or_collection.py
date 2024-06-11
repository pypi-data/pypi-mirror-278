from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_tag_or_collection(self, AUTH_TOKEN, URL, TYPE, TAG_ID, DEBUG):

    API_URL = f"{URL}/api/admin/{TYPE}/{TAG_ID}"
    
    return _send_request(self, AUTH_TOKEN, "delete tag or colleciton", API_URL, "DELETE", None, None, DEBUG)