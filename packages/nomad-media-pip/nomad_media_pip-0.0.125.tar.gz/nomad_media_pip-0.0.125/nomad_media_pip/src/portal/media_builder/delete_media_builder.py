from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_media_builder(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/mediaBuilder/{ID}"

    return _send_request(self, AUTH_TOKEN, "Delete Media Builder", API_URL, "DELETE", None, None, DEBUG)