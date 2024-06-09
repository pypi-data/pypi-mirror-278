from nomad_media_pip.src.helpers.send_request import _send_request

def _get_user_upload_parts(self, AUTH_TOKEN, URL, UPLOAD_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/upload/{UPLOAD_ID}"

    return _send_request(self, AUTH_TOKEN, "Get user upload parts", API_URL, "GET", None, None, DEBUG)