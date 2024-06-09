from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_content(self, AUTH_TOKEN, URL, ID, CONTENT_DEFINITION_ID, DEBUG):
  
    API_URL = f"{URL}/api/content/{ID}?contentDefinitionId={CONTENT_DEFINITION_ID}"
   
    return _send_request(self, AUTH_TOKEN, "Deleting content", API_URL, "DELETE", None, None, DEBUG)