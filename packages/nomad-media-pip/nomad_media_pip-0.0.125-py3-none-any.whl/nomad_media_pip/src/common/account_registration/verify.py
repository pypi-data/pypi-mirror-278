from nomad_media_pip.src.helpers.send_request import _send_request

def _verify(URL, EMAIL, CODE, DEBUG):
    API_URL = f"{URL}/api/account/verify"

    BODY = {
    	"userName": EMAIL, 
        "token": CODE
    }

    return _send_request(None, None, "Verification", API_URL, "POST", None, BODY, DEBUG)    