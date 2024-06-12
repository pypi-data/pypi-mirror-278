from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_output_profiles(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/api/liveOutputProfile"

    return _send_request(self, AUTH_TOKEN, "Get Live Output Profiles", API_URL, "GET", None, None, DEBUG)