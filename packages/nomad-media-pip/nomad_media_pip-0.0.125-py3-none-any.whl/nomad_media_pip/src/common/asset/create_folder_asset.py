from nomad_media_pip.src.helpers.send_request import _send_request

def _create_folder_asset(self, AUTH_TOKEN, URL, PARENT_ID, DISPLAY_NAME, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{PARENT_ID}/create-folder"

    BODY = {
        "displayName": DISPLAY_NAME
    }

    return _send_request(self, AUTH_TOKEN, "Create folder asset", API_URL, "POST", None, BODY, DEBUG)