from nomad_media_pip.src.helpers.send_request import _send_request

def _get_tag_or_collection(self, AUTH_TOKEN, URL, TYPE, ID, DEBUG):
        
    API_URL = f"{URL}/api/admin/{TYPE}/{ID}"
       
    return _send_request(self, AUTH_TOKEN, "Get Tag or Collection", API_URL, "GET", None, None, DEBUG)