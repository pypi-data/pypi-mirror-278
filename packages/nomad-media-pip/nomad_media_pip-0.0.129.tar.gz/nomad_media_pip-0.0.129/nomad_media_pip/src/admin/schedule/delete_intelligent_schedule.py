from nomad_media_pip.src.helpers.send_request import _send_request

def _delete_intelligent_schedule(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/admin/schedule/{ID}"

    return _send_request(self, AUTH_TOKEN, "Delete Intelligent Schedule", API_URL, "DELETE", None, None, DEBUG)