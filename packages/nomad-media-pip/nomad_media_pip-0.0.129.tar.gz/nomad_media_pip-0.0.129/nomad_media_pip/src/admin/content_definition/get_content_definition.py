from nomad_media_pip.src.helpers.send_request import _send_request

def _get_content_definition(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/contentDefinition/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get content definitions", API_URL, "GET", None, None, DEBUG)