from nomad_media_pip.src.helpers.send_request import _send_request

def _add_custom_properties(self, AUTH_TOKEN, URL, ID, NAME, DATE, CUSTOM_PROPERTIES, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ID}"

    BODY = {}

    if NAME: BODY["displayName"] = NAME
    if DATE: BODY["displayDate"] = DATE
    if CUSTOM_PROPERTIES: BODY["customProperties"] = CUSTOM_PROPERTIES

    return _send_request(self, AUTH_TOKEN, "Add Custom Properties", API_URL, "PATCH", None, BODY, DEBUG)