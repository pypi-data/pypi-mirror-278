from nomad_media_pip.src.helpers.send_request import _send_request

def _get_audit(self, AUTH_TOKEN, URL, ID, DEBUG):
    API_URL = f"{URL}/api/admin/audit/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get audit", API_URL, "GET", None, None, DEBUG)