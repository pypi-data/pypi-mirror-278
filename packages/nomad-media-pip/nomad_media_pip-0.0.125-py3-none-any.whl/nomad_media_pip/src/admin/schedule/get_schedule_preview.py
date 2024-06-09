from nomad_media_pip.src.helpers.send_request import _send_request

def _get_schedule_preview(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/admin/schedule/{ID}/preview"

    return _send_request(self, AUTH_TOKEN, "Get Schedule Preview", API_URL, "GET", None, None, DEBUG)