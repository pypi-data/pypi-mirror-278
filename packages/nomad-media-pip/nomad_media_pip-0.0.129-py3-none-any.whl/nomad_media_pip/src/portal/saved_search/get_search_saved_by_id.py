from nomad_media_pip.src.helpers.send_request import _send_request

def _get_search_saved_by_id(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/portal/search-saved/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get saved search", API_URL, "GET", None, None, DEBUG)