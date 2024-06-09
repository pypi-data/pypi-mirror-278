from nomad_media_pip.src.helpers.send_request import _send_request 

def _update_asset_language(self, AUTH_TOKEN, URL, ASSET_ID, LANGUAGE_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/language"

    BODY = {
        "languageId": LANGUAGE_ID
    }

    return _send_request(self, AUTH_TOKEN, "Update asset language", API_URL, "POST", None, BODY, DEBUG)
