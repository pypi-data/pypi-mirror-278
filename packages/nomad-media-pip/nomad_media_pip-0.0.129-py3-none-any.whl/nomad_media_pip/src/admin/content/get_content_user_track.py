from nomad_media_pip.src.helpers.send_request import _send_request

def _get_content_user_track(self, AUTH_TOKEN, URL, CONTENT_ID, CONTENT_DEFINITION_ID, SORT_COLUMN,
                         IS_DESC, PAGE_INDEX, SIZE_INDEX, DEBUG):
        
    API_URL = f"{URL}/api/content/{CONTENT_DEFINITION_ID}/user-track/{CONTENT_ID}"

    PARAMS = {
        "sortColumn": SORT_COLUMN,
        "isDesc": IS_DESC,
        "pageIndex": PAGE_INDEX,
        "sizeIndex": SIZE_INDEX
    }

    return _send_request(self, AUTH_TOKEN, "Get content user track", API_URL, "GET", PARAMS, None, DEBUG)