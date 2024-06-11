from nomad_media_pip.src.helpers.send_request import _send_request

def _create_content(self, AUTH_TOKEN, URL, CONTENT_DEFINITION_ID, LANGUAGE_ID, DEBUG):
  
    API_URL = f"{URL}/api/content/new?contentDefinitionId={CONTENT_DEFINITION_ID}"
    
    PARAMS = {
        "languageId": LANGUAGE_ID
    }
    
    return _send_request(self, AUTH_TOKEN, "Create content", API_URL, "GET", PARAMS, None, DEBUG)