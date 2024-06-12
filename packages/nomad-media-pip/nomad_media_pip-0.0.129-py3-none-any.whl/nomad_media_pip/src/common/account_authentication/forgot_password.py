from nomad_media_pip.src.helpers.send_request import _send_request

def _forgot_password(URL, USENAME, DEBUG):
    API_URL = f"{URL}/api/account/forgot-password"
  
    BODY = {
        "username": USENAME
    }
    
    return _send_request(None, None, "Forgot Password", API_URL, "POST", None, BODY, DEBUG)