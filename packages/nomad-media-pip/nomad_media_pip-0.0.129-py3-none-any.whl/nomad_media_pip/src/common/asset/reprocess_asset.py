from nomad_media_pip.src.helpers.send_request import _send_request 

def _reprocess_asset(self, AUTH_TOKEN, URL, TARGET_IDS, DEBUG):

    API_URL = f"{URL}/api/admin/asset/reprocess"

    BODY = {
        "target_ids": TARGET_IDS
    }

    return _send_request(self, AUTH_TOKEN, "Reprocess asset", API_URL, "POST", None, BODY, DEBUG)
    