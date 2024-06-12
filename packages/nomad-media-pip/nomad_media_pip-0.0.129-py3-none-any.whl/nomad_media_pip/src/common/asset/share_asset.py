from nomad_media_pip.src.helpers.send_request import _send_request 

def _share_asset(self, AUTH_TOKEN, URL, ASSET_ID, NOMAD_USERS, EXTERNAL_USERS,
                 SHARE_DURATION_IN_HOURS, DEBUG):
    
    API_URL = f"{URL}/api/asset/{ASSET_ID}/share"

    BODY = {
        "assetId": ASSET_ID,
        "nomadUsers": NOMAD_USERS,
        "externalUsers": EXTERNAL_USERS,
        "durationInHours": SHARE_DURATION_IN_HOURS
    }

    return _send_request(self, AUTH_TOKEN, "Share asset", API_URL, "POST", None, BODY, DEBUG)
    