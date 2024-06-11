from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_form(self, AUTH_TOKEN, URL, CONTENT_DEFINITION_ID, FORM_INFO, DEBUG):

    API_URL = f"{URL}/api/media/form/{CONTENT_DEFINITION_ID}"

    BODY = FORM_INFO

    return _send_request(self, AUTH_TOKEN, "Forms", API_URL, "POST", None, BODY, DEBUG)
    