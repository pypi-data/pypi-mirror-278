from nomad_media_pip.src.helpers.send_request import _send_request 

def _delete_related_content(self, AUTH_TOKEN, URL, CONTENT_ID, RELATED_CONTENT_ID, CONTENT_DEFINITION, 
                            API_TYPE, DEBUG):

    API_URL = f"{URL}/api/admin/related/delete" if API_TYPE == "admin" else f"{URL}/api/content/related/delete"

    BODY = {
        "items": [
            {
                "contentDefinition": CONTENT_DEFINITION,
                "contentId": CONTENT_ID,
                "relatedContentId": RELATED_CONTENT_ID
            }
        ]
    }

    return _send_request(self, AUTH_TOKEN, "delete related content", API_URL, "POST,", None, BODY, DEBUG)
    