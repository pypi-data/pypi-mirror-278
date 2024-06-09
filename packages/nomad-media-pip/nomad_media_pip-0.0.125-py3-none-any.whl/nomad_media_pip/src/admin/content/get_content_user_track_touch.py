from nomad_media_pip.src.helpers.send_request import _send_request

def _get_content_user_track_touch(self, AUTH_TOKEN, URL, CONTNET_ID, CONTENT_DEFINITION_ID, 
                                  DEBUG):
    API_URL = f"{URL}/api/content/{CONTENT_DEFINITION_ID}/user-track/{CONTNET_ID}/touch"

    return _send_request(self, AUTH_TOKEN, "Get content user track touch", API_URL, "GET", None, None, DEBUG)