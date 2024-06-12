from nomad_media_pip.src.helpers.send_request import _send_request 

def _create_media_builder_items_bulk(self, AUTH_TOKEN, URL, MEDIA_BUILDER_ID, MEDIA_BUILDER_ITEMS, DEBUG):

	API_URL = f"{URL}/api/mediaBuilder/{MEDIA_BUILDER_ID}/items/bulk"

	BODY = MEDIA_BUILDER_ITEMS
	
	return _send_request(self, AUTH_TOKEN, "Create Media Builder Items Bulk", API_URL, "POST", None, BODY, DEBUG)
	