from nomad_media_pip.src.helpers.send_request import _send_request

def _deactivate_content_user_track(self, AUTH_TOKEN, URL, SESSION_ID, CONTENT_ID,
                                CONTENT_DEFINITION_ID, DEACTIVATE, DEBUG):

    API_URL = f"{URL}/api/content/{CONTENT_DEFINITION_ID}/user-track/{CONTENT_ID}/{SESSION_ID}/{DEACTIVATE}"

    return _send_request(self, AUTH_TOKEN, "Deactivate content user track", API_URL, "DELETE", None, None, DEBUG)