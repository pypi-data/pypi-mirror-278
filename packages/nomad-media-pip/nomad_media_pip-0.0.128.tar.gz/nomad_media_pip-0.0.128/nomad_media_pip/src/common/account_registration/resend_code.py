from nomad_media_pip.src.helpers.send_request import _send_request

def _resend_code(URL, EMAIL, DEBUG):
	API_URL = f"{URL}/api/account/resend-code"

	BODY = {
		"userName": EMAIL
	}

	return _send_request(None, None, "Resend code", API_URL, "POST", None, BODY, DEBUG)	