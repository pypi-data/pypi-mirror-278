from nomad_media_pip.src.helpers.send_request import _send_request 

def _register_guest(self, AUTH_TOKEN, URL, EMAIL, FIRST_NAME, LAST_NAME, PASSWORD, DEBUG):
  
    API_URL = f"{URL}/api/account/register-guest"

    BODY = {
      	"email": EMAIL,
        "firstName": FIRST_NAME,
        "lastName": LAST_NAME,
        "password": PASSWORD
    }

    return _send_request(self, AUTH_TOKEN, "Registering guest", API_URL, "POST", None, BODY, DEBUG)
    