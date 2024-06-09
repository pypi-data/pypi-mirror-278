from nomad_media_pip.src.helpers.send_request import _send_request

def _register(URL, EMAIL, FIRST_NAME, LAST_NAME, PASSWORD, DEBUG):

	API_URL = f"{URL}/api/account/register"

	BODY = {
		"firstName": FIRST_NAME,
		"lastName": LAST_NAME,
		"email": EMAIL,
		"password": PASSWORD
	}

	return _send_request(None, None, "Register user", API_URL, "POST", None, BODY, DEBUG)	