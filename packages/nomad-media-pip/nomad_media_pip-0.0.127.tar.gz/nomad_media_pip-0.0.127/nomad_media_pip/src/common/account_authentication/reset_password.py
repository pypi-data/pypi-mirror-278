from nomad_media_pip.src.helpers.send_request import _send_request

def _reset_password(URL, USENAME, CODE, NEW_PASSWORD, DEBUG):
    API_URL = f"{URL}/api/account/reset-password"

    BODY = {
        "userName": USENAME,
        "token": CODE,
        "newPassword": NEW_PASSWORD
    }

    return _send_request(None, None, "Reset Password", API_URL, "POST", None, BODY, DEBUG)
   