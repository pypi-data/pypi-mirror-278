from nomad_media_pip.src.helpers.send_request import _send_request 
from nomad_media_pip.src.common.asset.get_asset_ad_breaks import _get_asset_ad_breaks

def _update_asset_ad_break(self, AUTH_TOKEN, URL, ASSET_ID, AD_BREAK_ID, TIME_CODE, TAGS, LABELS,
                           DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/adbreak/{AD_BREAK_ID}"

    ASSET_AD_BREAKS = _get_asset_ad_breaks(self, AUTH_TOKEN, URL, ASSET_ID, DEBUG)
    AD_BREAK = next((ad_break for ad_break in ASSET_AD_BREAKS if ad_break["id"] == AD_BREAK_ID), None)

    BODY = {
        "id": AD_BREAK_ID,
        "timecode": TIME_CODE or AD_BREAK.get("timecode"),
        "tags": TAGS or AD_BREAK.get("tags"),
        "labels": LABELS or AD_BREAK.get("labels")
    }

    return _send_request(self, AUTH_TOKEN, "Update ad break", API_URL, "PUT", None, BODY, DEBUG)
    