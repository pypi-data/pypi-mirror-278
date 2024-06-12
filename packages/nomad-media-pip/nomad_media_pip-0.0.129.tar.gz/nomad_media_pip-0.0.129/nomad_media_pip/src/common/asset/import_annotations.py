from nomad_media_pip.src.helpers.send_request import _send_request

def _import_annotations(self, AUTH_TOKEN, URL, ASSET_ID, ANNOTATIONS, DEBUG):

    API_URL = f"{URL}/api/asset/{ASSET_ID}/annotation/import"

    return _send_request(self, AUTH_TOKEN, "Import annotations", API_URL, "POST\nBODY: {json.dumps(ANNOTATIONS, indent=4)}", None, None, DEBUG)