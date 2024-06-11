from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_media_builder_item(self, AUTH_TOKEN, URL, ID, ITEM_ID, DEBUG):

    API_URL = f"{URL}/api/mediaBuilder/{ID}/items/{ITEM_ID}"

    return _send_request(self, AUTH_TOKEN, "Delete Media Builder Item", API_URL, "DELETE", None, None, DEBUG)