from nomad_media_pip.src.helpers.send_request import _send_request 

def _rename_content_group(self, AUTH_TOKEN, URL, ID, NAME, DEBUG):
  
	API_URL = f"{URL}/api/contentGroup/{ID}"

	BODY = {
		"Name": NAME
	}
	
	return _send_request(self, AUTH_TOKEN, "Rename content group", API_URL, "PATCH", None, BODY, DEBUG)
	