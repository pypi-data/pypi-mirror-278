from nomad_media_pip.src.helpers.send_request import _send_request 
from nomad_media_pip.src.portal.media_builder.get_media_builder import _get_media_builder

def _update_media_builder(self, AUTH_TOKEN, URL, ID, NAME, DESTINATION_FOLDER_ID, COLLECTIONS,
                          RELATED_CONTENT, TAGS, PROPERTIES, DEBUG):
    
    API_URL = f"{URL}/api/mediaBuilder/{ID}"

    INFO = _get_media_builder(self, AUTH_TOKEN, URL, ID, DEBUG)

    BODY = {
        "name": NAME or INFO.get("name"),
        "destinationFolderId": DESTINATION_FOLDER_ID or INFO.get("destinationFolderId"),
        "collections": COLLECTIONS or INFO.get("collections"),
        "relatedContent": RELATED_CONTENT or INFO.get("relatedContent"),
        "tags": TAGS or INFO.get("tags"),
        "properties": PROPERTIES or INFO.get("properties")
    }

    return _send_request(self, AUTH_TOKEN, "Update Media Builder", API_URL, "PUT,", None, BODY, DEBUG)
    