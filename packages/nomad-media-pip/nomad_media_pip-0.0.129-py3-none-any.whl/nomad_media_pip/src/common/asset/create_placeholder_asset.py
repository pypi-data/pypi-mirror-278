from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_placeholder_asset(self, AUTH_TOKEN, URL, PARENT_ID, ASSET_NAME, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{PARENT_ID}/create-placeholder"

    BODY = {
        "assetName": ASSET_NAME
    }

    return _send_request(self, AUTH_TOKEN, "Create placeholder asset", API_URL, "POST", None, BODY, DEBUG)
    