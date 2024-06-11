from nomad_media_pip.src.helpers.send_request import _send_request

def _get_media_builder_ids_from_asset(self, AUTH_TOKEN, URL, SOURCE_ASSET_ID, DEBUG):

	API_URL = f"{URL}/api/mediaBuilder/idsbysource/{SOURCE_ASSET_ID}"

	return _send_request(self, AUTH_TOKEN, "Get Media Builder Ids From Asset", API_URL, "GET", None, None, DEBUG)