from nomad_media_pip.src.helpers.send_request import _send_request

def _get_content_groups(self, AUTH_TOKEN, URL, DEBUG):
  
    API_URL = f"{URL}/api/contentGroup"
   
    return _send_request(self, AUTH_TOKEN, "Get content groups", API_URL, "GET", None, None, DEBUG)