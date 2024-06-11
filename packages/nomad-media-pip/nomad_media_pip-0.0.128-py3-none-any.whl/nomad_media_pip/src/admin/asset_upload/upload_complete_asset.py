from nomad_media_pip.src.helpers.send_request import _send_request

def _upload_complete_asset(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/asset/upload/{ID}/complete"
    
    return _send_request(self, AUTH_TOKEN, "Upload Complete Asset", API_URL, "POST", None, None, DEBUG)