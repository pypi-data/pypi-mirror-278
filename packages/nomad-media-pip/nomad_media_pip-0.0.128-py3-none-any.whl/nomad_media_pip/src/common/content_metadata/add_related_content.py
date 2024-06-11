from nomad_media_pip.src.helpers.send_request import _send_request 

def _add_related_content(self, AUTH_TOKEN, URL, CONTENT_ID, RELATED_CONTENT_ID, CONTENT_DEFINITION, 
                         API_TYPE, DEBUG):

    API_URL = f"{URL}/api/admin/related" if API_TYPE == "admin" else f"{URL}/api/content/related"

    BODY = {
        "items": [
            {
                "contentDefinition": CONTENT_DEFINITION,
                "contentId": CONTENT_ID,
                "relatedContentId": RELATED_CONTENT_ID
            }
        ]
    }

    return _send_request(self, AUTH_TOKEN, "add related content", API_URL, "POST,", None, BODY, DEBUG)
    