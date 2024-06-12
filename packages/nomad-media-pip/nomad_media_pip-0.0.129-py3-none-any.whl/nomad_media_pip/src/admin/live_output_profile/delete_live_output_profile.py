from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_live_output_profile(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/liveOutputProfile/{ID}"

    return _send_request(self, AUTH_TOKEN, "Delete Live Output Profile", API_URL, "DELETE", None, None, DEBUG)