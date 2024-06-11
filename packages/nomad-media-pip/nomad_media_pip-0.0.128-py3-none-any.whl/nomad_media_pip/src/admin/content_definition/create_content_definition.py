from nomad_media_pip.src.helpers.send_request import _send_request

def _create_content_definition(self, AUTH_TOKEN, URL, DEBUG):

    CREATE_NEW_API_URL = f"{URL}/api/contentDefinition/New"

    return _send_request(self, AUTH_TOKEN, "Create content definition", CREATE_NEW_API_URL, "GET", None, None, DEBUG)
        

    