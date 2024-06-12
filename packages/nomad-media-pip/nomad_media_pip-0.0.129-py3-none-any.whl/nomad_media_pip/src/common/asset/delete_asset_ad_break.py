from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_asset_ad_break(self, AUTH_TOKEN, URL, ASSET_ID, AD_BREAK_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/adbreak/{AD_BREAK_ID}"

    return _send_request(self, AUTH_TOKEN, "Delete asset ad break", API_URL, "DELETE", None, None, DEBUG)