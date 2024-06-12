from nomad_media_pip.src.helpers.send_request import _send_request 

def _duplicate_media_builder(self, AUTH_TOKEN, URL, ID, NAME, DESTINATION_FOLDER_ID, COLLECTIONS,
                             RELATED_CONTENTS, PROPERTIES, DEBUG):
    
    API_URL = f"{URL}/api/mediaBuilder/{ID}/duplicate"

    BODY = {
        "name": NAME,
        "destinationFolderId": DESTINATION_FOLDER_ID,
        "collections": COLLECTIONS,
        "relatedContent": RELATED_CONTENTS,
        "properties": PROPERTIES
    }

    return _send_request(self, AUTH_TOKEN, "Duplicate Media Builder", API_URL, "POST,", None, BODY, DEBUG)
    