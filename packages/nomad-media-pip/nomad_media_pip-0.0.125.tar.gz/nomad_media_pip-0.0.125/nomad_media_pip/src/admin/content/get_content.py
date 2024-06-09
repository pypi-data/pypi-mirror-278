from nomad_media_pip.src.helpers.send_request import _send_request

def _get_content(self, AUTH_TOKEN, URL, ID, CONTENT_DEFINITION_ID, IS_REVISION, DEBUG):
    API_URL = f"{URL}/api/content/{ID}?contentDefinitionId={CONTENT_DEFINITION_ID}"
   
    PARAMS = {
        "isRevision": IS_REVISION
    }
    
    return _send_request(self, AUTH_TOKEN, "Get content", API_URL, "GET", PARAMS, None, DEBUG)