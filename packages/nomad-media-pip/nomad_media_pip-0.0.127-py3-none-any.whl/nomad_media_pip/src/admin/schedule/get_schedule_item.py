from nomad_media_pip.src.helpers.send_request import _send_request

def _get_schedule_item(self, AUTH_TOKEN, URL, ID, ITEM_ID, DEBUG):
    
    API_URL = f"{URL}/api/admin/schedule/{ID}/item/{ITEM_ID}"

    return _send_request(self, AUTH_TOKEN, "Get Schedule Item", API_URL, "GET", None, None, DEBUG)