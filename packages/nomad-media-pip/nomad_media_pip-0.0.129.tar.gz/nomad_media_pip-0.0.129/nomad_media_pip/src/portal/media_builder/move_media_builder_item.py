from nomad_media_pip.src.helpers.send_request import _send_request 

def _move_media_builder_item(self, AUTH_TOKEN, URL, ID, ITEM_ID, PREVIOUS_ITEM_ID, DEBUG):

    API_URL = f"{URL}/api/mediaBuilder/{ID}/items/{ITEM_ID}/move"

    BODY = {
        "previousItemId": PREVIOUS_ITEM_ID
    }

    return _send_request(self, AUTH_TOKEN, "Move Media Builder Item", API_URL, "POST", None, BODY, DEBUG)
    