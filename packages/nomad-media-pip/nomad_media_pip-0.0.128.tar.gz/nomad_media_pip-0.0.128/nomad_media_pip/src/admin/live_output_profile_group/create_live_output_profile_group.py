from nomad_media_pip.src.helpers.send_request import _send_request

def _create_live_output_profile_group(self, AUTH_TOKEN, URL, NAME, IS_ENABLED, MANIFEST_TYPE, IS_DEFAULT_GROUP, LIVE_OUTPUT_TYPE, ARCHIVE_LIVE_OUTPUT_PROFILE, LIVE_OUTPUT_PROFILES, DEBUG):

	API_URL = f"{URL}/api/liveOutputProfileGroup"

	BODY = {
		"name": NAME,
		"enabled": IS_ENABLED,
		"manifestType": MANIFEST_TYPE,
		"isDefaultGroup": IS_DEFAULT_GROUP,
		"outputType": LIVE_OUTPUT_TYPE,
		"archiveOutputProfile": ARCHIVE_LIVE_OUTPUT_PROFILE,
		"outputProfiles": LIVE_OUTPUT_PROFILES
	}

	return _send_request(self, AUTH_TOKEN, "Create live output profile group", API_URL, "POST", None, BODY, DEBUG)