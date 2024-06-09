from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_user(self, AUTH_TOKEN, URL, USER_ID, DEBUG):

    API_URL = f"{URL}/api/admin/user/{USER_ID}"

    return _send_request(self, AUTH_TOKEN, "Delete User", API_URL, "DELETE", None, None, DEBUG)