from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_live_output_profile_group(self, AUTH_TOKEN, URL, LIVE_OUTPUT_PROFILE_GROUP_ID, DEBUG):

	API_URL = f"{URL}/api/liveOutputProfileGroup/{LIVE_OUTPUT_PROFILE_GROUP_ID}"

	return _send_request(self, AUTH_TOKEN, "Delete Live Output Profile Group", API_URL, "DELETE", None, None, DEBUG)