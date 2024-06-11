from nomad_media_pip.src.helpers.send_request import _send_request 

def _media_search(self, AUTH_TOKEN, URL, SEARCH_QUERY, IDS, SORT_FIELDS, OFFSET, SIZE, DEBUG):

    API_URL = f"{URL}/api/media/search"

    BODY = {
        key: value  for key, value in {
            "searchQuery": SEARCH_QUERY,
            "ids": IDS, 
            "sortFields": SORT_FIELDS,
            "offset": OFFSET,
            "size": SIZE
        }.items() if value is not None
    }

    return _send_request(self, AUTH_TOKEN, "Media search", API_URL, "POST", None, BODY, DEBUG)
    