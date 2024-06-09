from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_output_types(self, AUTH_TOKEN, URL, DEBUG):
    API_URL = f"{URL}/api/lookup/117"

    return _send_request(self, AUTH_TOKEN, "Get Output Types", API_URL, "GET", None, None, DEBUG)