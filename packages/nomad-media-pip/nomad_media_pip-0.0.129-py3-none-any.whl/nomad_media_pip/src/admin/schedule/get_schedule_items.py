from nomad_media_pip.src.helpers.send_request import _send_request

def _get_schedule_items(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/admin/schedule/{ID}/items"

    return _send_request(self, AUTH_TOKEN, "Get Schedule Items", API_URL, "GET", None, None, DEBUG)