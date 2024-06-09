from nomad_media_pip.src.helpers.send_request import _send_request

def _get_content_definition_types(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/lookup/6"

    return _send_request(self, AUTH_TOKEN, "Get content definition types", API_URL, "GET", None, None, DEBUG)