from nomad_media_pip.src.helpers.send_request import _send_request

def _move_schedule_item(self, AUTH_TOKEN, URL, ID, ITEM_ID, PREVIOUS_ITEM, DEBUG):
    
    API_URL = f"{URL}/api/admin/schedule/{ID}/item/{ITEM_ID}/move"
    
    BODY = {
        "previous_item": PREVIOUS_ITEM
    }

    return _send_request(self, AUTH_TOKEN, "Move Schedule Item", API_URL, "POST", None, BODY, DEBUG)