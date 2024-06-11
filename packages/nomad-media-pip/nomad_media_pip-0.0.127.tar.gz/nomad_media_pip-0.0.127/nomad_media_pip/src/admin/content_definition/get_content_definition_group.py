from nomad_media_pip.src.helpers.send_request import _send_request

def _get_content_definition_group(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/contentDefinitionGroup"

    return _send_request(self, AUTH_TOKEN, "Get content definition group", API_URL, "GET", None, None, DEBUG)