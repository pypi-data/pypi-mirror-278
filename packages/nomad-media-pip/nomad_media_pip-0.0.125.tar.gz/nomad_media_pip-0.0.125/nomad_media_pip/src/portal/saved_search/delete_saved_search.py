from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_saved_search(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/portal/savedsearch/{ID}"

    return _send_request(self, AUTH_TOKEN, "Delete saved search", API_URL, "DELETE", None, None, DEBUG)