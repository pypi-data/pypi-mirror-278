from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_content_group(self, AUTH_TOKEN, URL, CONTENT_GROUP_ID, DEBUG):
  
    API_URL = f"{URL}/api/contentGroup/{CONTENT_GROUP_ID}"

    return _send_request(self, AUTH_TOKEN, "Delete content group", API_URL, "DELETE", None, None, DEBUG)