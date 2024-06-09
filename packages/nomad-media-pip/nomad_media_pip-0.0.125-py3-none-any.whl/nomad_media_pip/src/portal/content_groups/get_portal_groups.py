from nomad_media_pip.src.helpers.send_request import _send_request 

def _get_portal_groups(self, AUTH_TOKEN, URL, RETURNED_GROUP_NAMES, DEBUG):
	API_URL = f"{URL}/api/portal/groups"

	BODY = {
		"returnedGroupNames": RETURNED_GROUP_NAMES
	}

	return _send_request(self, AUTH_TOKEN, "Get poral groups", API_URL, "POST", None, BODY, DEBUG)
	