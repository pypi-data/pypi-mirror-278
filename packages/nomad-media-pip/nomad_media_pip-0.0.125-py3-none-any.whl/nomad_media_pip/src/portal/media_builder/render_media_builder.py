from nomad_media_pip.src.helpers.send_request import _send_request

def _render_media_builder(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/mediaBuilder/{ID}/render"

    return _send_request(self, AUTH_TOKEN, "Render Media Builder", API_URL, "POST", None, None, DEBUG)