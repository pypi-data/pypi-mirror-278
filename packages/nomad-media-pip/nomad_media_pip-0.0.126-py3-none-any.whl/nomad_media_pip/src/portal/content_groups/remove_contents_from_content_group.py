from nomad_media_pip.src.helpers.send_request import _send_request 

def _remove_contents_from_content_group(self, AUTH_TOKEN, URL, CONTENT_GROUP_ID, CONTENTS, DEBUG):
  
	API_URL = f"{URL}/api/contentGroup/remove/{CONTENT_GROUP_ID}"

	BODY = CONTENTS

	return _send_request(self, AUTH_TOKEN, "Remove content to content group", API_URL, "POST", None, BODY, DEBUG)
	