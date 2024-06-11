from nomad_media_pip.src.helpers.send_request import _send_request 

def _guest_invite(self, AUTH_TOKEN, URL, CONTENT_ID, CONTENT_DEFINITION_ID, 
                 USER_ID, EMAILS, CONTENT_SECURITY_ATTRIBUTE, DEBUG):
        
    API_URL = f"{URL}/api/account/invite-user"

    BODY = {
        "contentId": CONTENT_ID,
      	"contentDefinitionId": CONTENT_DEFINITION_ID,
        "userId": USER_ID,
        "emails": EMAILS,
        "contentSecurityAttribute": CONTENT_SECURITY_ATTRIBUTE
    }

    return _send_request(self, AUTH_TOKEN, "Guest invite", API_URL, "POST", None, BODY, DEBUG)
    