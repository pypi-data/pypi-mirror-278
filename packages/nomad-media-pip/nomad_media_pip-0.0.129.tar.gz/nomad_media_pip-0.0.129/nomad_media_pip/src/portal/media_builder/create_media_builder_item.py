from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_media_builder_item(self, AUTH_TOKEN, URL, ID, SOURCE_ASSET_ID, START_TIME_CODE,
                               END_TIME_CODE, SOURCE_ANNOATION_ID, RELATED_CONTENTS, DEBUG):
    
    API_URL = f"{URL}/api/mediaBuilder/{ID}/items"

    BODY = {
        "sourceAssetId": SOURCE_ASSET_ID,
        "startTimeCode": START_TIME_CODE,
        "endTimeCode": END_TIME_CODE,
        "sourceAnnotationId": SOURCE_ANNOATION_ID,
        "relatedContent": RELATED_CONTENTS
    }

    return _send_request(self, AUTH_TOKEN, "Create Media Builder Item", API_URL, "POST,", None, BODY, DEBUG)
    