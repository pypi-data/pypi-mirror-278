from nomad_media_pip.src.helpers.send_request import _send_request

def _get_security_groups(self, AUTH_TOKEN, URL, DEBUG):
    API_URL = f"{URL}/api/lookup/22?lookupKey=99e8767a-00ba-4758-b9c2-e07b52c47016"

    return _send_request(self, AUTH_TOKEN, "Get Security Groups", API_URL, "GET", None, None, DEBUG)