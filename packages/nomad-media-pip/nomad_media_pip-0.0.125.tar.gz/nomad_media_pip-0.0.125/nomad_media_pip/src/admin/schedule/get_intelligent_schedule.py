from nomad_media_pip.src.helpers.send_request import _send_request

def _get_intelligent_schedule(self, AUTH_TOKEN, URL, ID, DEBUG):
    
    API_URL = f"{URL}/api/admin/schedule/{ID}"

    return _send_request(self, AUTH_TOKEN, "Get Intelligent Schedule", API_URL, "GET", None, None, DEBUG)