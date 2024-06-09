from nomad_media_pip.src.helpers.send_request import _send_request

def _get_playlist(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/admin/schedule/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get Playlist", API_URL, "GET", None, None, DEBUG)