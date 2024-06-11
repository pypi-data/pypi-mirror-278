from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_output_profile_groups(self, AUTH_TOKEN, URL, DEBUG):

	API_URL = f"{URL}/api/liveOutputProfileGroup"

	return _send_request(self, AUTH_TOKEN, "Get Live Output Profile Groups", API_URL, "GET", None, None, DEBUG)