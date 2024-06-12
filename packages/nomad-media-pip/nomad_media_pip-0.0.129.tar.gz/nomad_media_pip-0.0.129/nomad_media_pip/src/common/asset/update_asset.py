from nomad_media_pip.src.helpers.send_request import _send_request 

def _update_asset(self, AUTH_TOKEN, URL, ASSET_ID, DISPLAY_NAME, DISPLAY_DATE, AVAILABLE_START_DATE,
                  AVAILABLE_END_DATE, CUSTOM_PROPERTIES, DEBUG):
    
    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}"

    BODY = {
        "displayName": DISPLAY_NAME,
        "displayDate": DISPLAY_DATE,
        "availableStartDate": AVAILABLE_START_DATE,
        "availableEndDate": AVAILABLE_END_DATE,
        "customProperties": CUSTOM_PROPERTIES
    }

    return _send_request(self, AUTH_TOKEN, "Update asset", API_URL, "PATCH", None, BODY, DEBUG)
    