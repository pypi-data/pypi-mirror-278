from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_event(self, AUTH_TOKEN, URL, ID, CONTENT_DEFINITION_ID, DEBUG):
    
    API_URL = f"{URL}/api/content/{ID}?contentDefinitionId={CONTENT_DEFINITION_ID}"

    return _send_request(self, AUTH_TOKEN, "Delete Event", API_URL, "DELETE", None, None, DEBUG)