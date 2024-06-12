from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_user_content_security_data(self, AUTH_TOKEN, URL, CONTENT_ID, CONTENT_DEFINITION_ID, USER_ID, EMAIL, ID, KEY_NAME, EXPIRATON_DATE, DEBUG):
    
    API_URL = f"{URL}/api/admin/user/userContentSecurity/delete"
       
    BODY = {
        "contentId": CONTENT_ID,
        "contentDefinitionId": CONTENT_DEFINITION_ID,
        "userId": USER_ID,
        "email": EMAIL,
        "id": ID,
        "keyName": KEY_NAME,
        "expirationDate": EXPIRATON_DATE
    }
    
    return _send_request(self, AUTH_TOKEN, "Delete User Content Security Data", API_URL, "POST", None, BODY, DEBUG)