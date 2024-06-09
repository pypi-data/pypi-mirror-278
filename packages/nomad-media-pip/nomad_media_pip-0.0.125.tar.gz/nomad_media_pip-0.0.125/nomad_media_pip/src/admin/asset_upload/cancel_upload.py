from nomad_media_pip.src.helpers.send_request import _send_request

def _cancel_upload(self, AUTH_TOKEN, URL, ID, DEBUG):
    API_URL = f"{URL}/api/asset/upload/{ID}/cancel"

    return _send_request(self, AUTH_TOKEN, "Cancel Upload", API_URL, "POST", None, None, DEBUG) 