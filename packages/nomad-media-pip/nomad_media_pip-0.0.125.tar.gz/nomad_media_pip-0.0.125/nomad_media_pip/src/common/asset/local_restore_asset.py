from nomad_media_pip.src.helpers.send_request import _send_request 

def _local_restore_asset(self, AUTH_TOKEN, URL, ASSET_ID, PROFILE, DEBUG):

    API_URL = f"{URL}/api/asset/{ASSET_ID}/localRestore"

    BODY = {
        "profile": PROFILE
    }

    return _send_request(self, AUTH_TOKEN, "Local restore asset", API_URL, "POST", None, BODY, DEBUG)
    