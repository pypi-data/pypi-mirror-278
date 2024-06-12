from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_operator.wait_for_live_operator_status import _wait_for_live_operator_status

def _start_broadcast(self, AUTH_TOKEN, URL, ID, PREROLL_ASSET_ID, POSTROLL_ASSET_ID, LIVE_INPUT_ID, 
                    RELATED_CONTENT_IDS, TAG_IDS, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/start"
    
    BODY = {
        "id": ID
    }

    if LIVE_INPUT_ID: BODY["liveInput"] = { "id": LIVE_INPUT_ID }
    if PREROLL_ASSET_ID: BODY["prerollAsset"] = { "id": PREROLL_ASSET_ID }
    if POSTROLL_ASSET_ID: BODY["postrollAsset"] = { "id": POSTROLL_ASSET_ID }

    if RELATED_CONTENT_IDS and isinstance(RELATED_CONTENT_IDS, list) and len(RELATED_CONTENT_IDS) > 0:
        BODY["relatedContent"] = [{"id": id} for id in RELATED_CONTENT_IDS]

    if TAG_IDS and isinstance(TAG_IDS, list) and len(TAG_IDS) > 0:
        BODY["tags"] = [{"id": id} for id in TAG_IDS]

    return _send_request(self, AUTH_TOKEN, "Start Broadcast", API_URL, "POST", BODY, None, DEBUG)