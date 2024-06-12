from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_user_content_attribute_data(self, AUTH_TOKEN, URL, USER_ID, DEBUG):
        
    API_URL = f"{URL}/api/admin/user/userContentAttribute/{USER_ID}"
    
    return _send_request(self, AUTH_TOKEN, "Delete User Content Attribute Data", API_URL, "DELETE", None, None, DEBUG)