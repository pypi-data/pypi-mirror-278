from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_media_builder(self, AUTH_TOKEN, URL, NAME, DESTINATION_FOLDER_ID, COLLECTIONS,
                          RELATED_CONTENT, TAGS, PROPERTIES, DEBUG):
    
    API_URL = f"{URL}/api/mediaBuilder"

    BODY = {
        "name": NAME,
        "destinationFolderId": DESTINATION_FOLDER_ID,
        "collections": COLLECTIONS,
        "relatedContent": RELATED_CONTENT,
        "tags": TAGS,
        "properties": PROPERTIES
    }

    return _send_request(self, AUTH_TOKEN, "Create Media Builder", API_URL, "POST,", None, BODY, DEBUG)
    