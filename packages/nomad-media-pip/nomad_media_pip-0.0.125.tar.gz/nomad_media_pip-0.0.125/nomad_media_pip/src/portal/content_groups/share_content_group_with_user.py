from nomad_media_pip.src.helpers.send_request import _send_request 

def _share_content_group_with_user(self, AUTH_TOKEN, URL, CONTENT_GROUP_ID, USER_IDS, DEBUG):
  
	API_URL = f"{URL}/api/contentGroup/share/{CONTENT_GROUP_ID}"

	BODY = USER_IDS
	
	return _send_request(self, AUTH_TOKEN, "Share content group with user", API_URL, "POST", None, BODY, DEBUG)
	