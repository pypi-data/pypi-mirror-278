from nomad_media_pip.src.helpers.send_request import _send_request

def _get_content_definitions(self, AUTH_TOKEN, URL, CONTENT_MANAGEMENT_TYPE, SORT_COLUMN, IS_DESC, PAGE_INDEX, PAGE_SIZE, DEBUG):

    API_URL = f"{URL}/api/contentDefinition"

    PARAMS = {
        "contentManagementType": CONTENT_MANAGEMENT_TYPE,
        "sortColumn": SORT_COLUMN,
        "isDesc": IS_DESC,
        "pageIndex": PAGE_INDEX,
        "pageSize": PAGE_SIZE
    }

    return _send_request(self, AUTH_TOKEN, "Getting Content Definitions", API_URL, "GET", PARAMS, None, DEBUG)