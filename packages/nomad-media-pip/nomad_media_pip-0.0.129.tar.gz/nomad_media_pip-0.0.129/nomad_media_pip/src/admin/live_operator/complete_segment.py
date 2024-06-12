from nomad_media_pip.src.helpers.send_request import _send_request

def _complete_segment(self, AUTH_TOKEN, URL, ID, RELATED_CONTENT_IDS, TAG_IDS, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/{ID}/completeSegment"

    BODY = {
        "liveOperatorId": ID,
    }

    if RELATED_CONTENT_IDS and isinstance(RELATED_CONTENT_IDS, list) and len(RELATED_CONTENT_IDS) > 0:
        BODY["relatedContent"] = [{"id": id} for id in RELATED_CONTENT_IDS]
    
    if TAG_IDS and isinstance(TAG_IDS, list) and len(TAG_IDS) > 0:
        BODY["tags"] = [{"id": id} for id in RELATED_CONTENT_IDS]

    return _send_request(self, AUTH_TOKEN, "Complete Segment", API_URL, "POST", BODY, None, DEBUG)