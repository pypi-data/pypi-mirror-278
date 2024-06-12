from nomad_media_pip.src.helpers.send_request import _send_request

def _get_asset_child_nodes(self, AUTH_TOKEN, URL, ID, FOLDER_ID, SORT_COLUMN, IS_DESC, PAGE_INDEX,
                           PAGE_SIZE, DEBUG):
    
    API_URL = f"{URL}/api/admin/asset/{ID}/getAssetChildNodes"

    PARAMS = {
        "folderId": FOLDER_ID,
        "sortColumn": SORT_COLUMN,
        "isDesc": IS_DESC,
        "pageIndex": PAGE_INDEX,
        "pageSize": PAGE_SIZE
    }   

    return _send_request(self, AUTH_TOKEN, "Get asset child nodes", API_URL, "GET", PARAMS, None, DEBUG)

