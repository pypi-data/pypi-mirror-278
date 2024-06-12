from nomad_media_pip.src.helpers.send_request import _send_request

def _create_media_builder_items_add_annotations(self, AUTH_TOKEN, URL, MEDIA_BUILDER_ID, SOURCE_ASSET_ID, DEBUG):

	API_URL = f"{URL}/api/mediaBuilder/{MEDIA_BUILDER_ID}/items/{SOURCE_ASSET_ID}/add-annotations"

	return _send_request(self, AUTH_TOKEN, "Create Media Builder Items Add Annotations", API_URL, "POST", None, None, DEBUG)