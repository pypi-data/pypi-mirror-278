from nomad_media_pip.src.helpers.send_request import _send_request 

def _patch_saved_search(self, AUTH_TOKEN, URL, ID, NAME, FEATURED, BOOKMARKED, PUBLIC, SEQUENCE, 
                        DEBUG):

    API_URL = f"{URL}/api/portal/savedsearch/{ID}"

    BODY = {
        key: value for key, value in {
            "name": NAME,
            "featured": FEATURED,
            "bookmarked": BOOKMARKED,
            "public": PUBLIC,
            "sequence": SEQUENCE
        }.items() if value is not None
    }

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + AUTH_TOKEN
    }

    return _send_request(self, AUTH_TOKEN, "Patch saved search", API_URL, "PATCH", None, BODY, DEBUG)
    