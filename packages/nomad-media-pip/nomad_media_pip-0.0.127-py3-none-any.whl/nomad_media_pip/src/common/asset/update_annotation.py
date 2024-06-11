from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.common.asset.get_annotations import _get_annotations

def _update_annotation(self, AUTH_TOKEN, URL, ASSET_ID, ANNOTATION_ID, START_TIME_CODE, 
                       END_TIME_CODE, FIRST_KEYWORD, SECOND_KEYWORD, DESCRIPTION, COUNTRY,
                       CONTENT_ID, IMAGE_URL, DEBUG):
    
    API_URL = f"{URL}/api/asset/{ASSET_ID}/annotation/{ANNOTATION_ID}"


    ASSET_ANNOTATIONS = _get_annotations(self, AUTH_TOKEN, URL, ASSET_ID, DEBUG)
    ANNOTATION = next((annotation for annotation in ASSET_ANNOTATIONS if annotation["id"] == ANNOTATION_ID), None)

    BODY = {
        "id": ANNOTATION_ID,
        "startTimeCode": START_TIME_CODE or ANNOTATION.get("startTimeCode"),
        "endTimeCode": END_TIME_CODE or ANNOTATION.get("endTimeCode"),
        "properties": {
            "firstKeyword": FIRST_KEYWORD or ANNOTATION.get("properties").get("firstKeyword"),
            "secondKeyword": SECOND_KEYWORD or ANNOTATION.get("properties").get("secondKeyword"),
            "description": DESCRIPTION or ANNOTATION.get("properties").get("description"),
            "country": COUNTRY or ANNOTATION.get("properties").get("country")
        },
        "contentId": CONTENT_ID or ANNOTATION.get("contentId"),
        "imageUrl": IMAGE_URL or ANNOTATION.get("imageUrl")
    }

    return _send_request(self, AUTH_TOKEN, "Update annotation", API_URL, "PUT", None, BODY, DEBUG)