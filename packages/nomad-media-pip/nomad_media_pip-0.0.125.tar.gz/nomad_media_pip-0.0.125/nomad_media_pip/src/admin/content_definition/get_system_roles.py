from nomad_media_pip.src.helpers.send_request import _send_request

def _get_system_roles(AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/lookup/45"

    return _send_request(None, AUTH_TOKEN, "Get system roles", API_URL, "GET", None, None, DEBUG)