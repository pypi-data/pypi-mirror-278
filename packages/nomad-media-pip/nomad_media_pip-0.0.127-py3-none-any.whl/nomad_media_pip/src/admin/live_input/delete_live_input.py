from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_live_input(self, AUTH_TOKEN, URL, INPUT_ID, DEBUG):
    API_URL = f"{URL}/api/liveInput/{INPUT_ID}"

    return _send_request(self, AUTH_TOKEN, "Delete Live Input", API_URL, "DELETE", None, None, DEBUG)
