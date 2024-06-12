from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_annotation(self, AUTH_TOKEN, URL, ASSET_ID, ANNOTATION_ID, DEBUG):

    API_URL = f"{URL}/api/asset/{ASSET_ID}/annotation/{ANNOTATION_ID}"

    return _send_request(self, AUTH_TOKEN, "Delete annotation", API_URL, "DELETE", None, None, DEBUG)