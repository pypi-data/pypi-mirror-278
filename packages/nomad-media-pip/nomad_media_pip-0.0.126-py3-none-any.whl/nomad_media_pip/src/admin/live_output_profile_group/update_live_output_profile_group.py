from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_output_profile_group.get_live_output_profile_group import _get_live_output_profile_group

def _update_live_output_profile_group(self, AUTH_TOKEN, URL, LIVE_OUTPUT_PROFILE_GROUP_ID, NAME, IS_ENABLED, MANIFEST_TYPE, IS_DEFAULT_GROUP, LIVE_OUTPUT_TYPE, ARCHIVE_LIVE_OUTPUT_PROFILE, LIVE_OUTPUT_PROFILES, DEBUG):

	API_URL = f"{URL}/api/liveOutputProfileGroup"

	PROFILE_GROUP_INFO = _get_live_output_profile_group(self, AUTH_TOKEN, URL, LIVE_OUTPUT_PROFILE_GROUP_ID, DEBUG)

	BODY = {
		"id": LIVE_OUTPUT_PROFILE_GROUP_ID or PROFILE_GROUP_INFO.get("id"),
		"name": NAME or PROFILE_GROUP_INFO.get("name"),
		"isEnabled": IS_ENABLED or PROFILE_GROUP_INFO.get("isEnabled"),
		"manifestType": MANIFEST_TYPE or PROFILE_GROUP_INFO.get("manifestType"),
		"isDefaultGroup": IS_DEFAULT_GROUP or PROFILE_GROUP_INFO.get("isDefaultGroup"),
		"outputType": LIVE_OUTPUT_TYPE or PROFILE_GROUP_INFO.get("outputType"),
		"archiveOutputProfile": ARCHIVE_LIVE_OUTPUT_PROFILE or PROFILE_GROUP_INFO.get("archiveOutputProfile"),
		"outputProfiles": LIVE_OUTPUT_PROFILES or PROFILE_GROUP_INFO.get("outputProfiles")
	}

	return _send_request(self, AUTH_TOKEN, "Update live output profile group", API_URL, "PUT", None, BODY, DEBUG)	