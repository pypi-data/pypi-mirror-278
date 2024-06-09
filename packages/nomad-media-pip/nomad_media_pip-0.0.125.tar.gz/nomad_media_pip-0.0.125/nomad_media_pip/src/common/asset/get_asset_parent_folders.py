from nomad_media_pip.src.helpers.send_request import _send_request

def _get_asset_parent_folders(self, AUTH_TOKEN, URL, ASSET_ID, PAGE_SIZE, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/parent-folders"

    PARAMS = {
        "pageSize": PAGE_SIZE
    }
   
    return _send_request(self, AUTH_TOKEN, "Get asset parent folders", API_URL, "GET", PARAMS, None, DEBUG)