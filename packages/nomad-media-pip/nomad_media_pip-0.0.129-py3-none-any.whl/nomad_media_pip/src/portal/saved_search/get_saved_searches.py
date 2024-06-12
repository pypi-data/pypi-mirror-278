from nomad_media_pip.src.helpers.send_request import _send_request

def _get_saved_searches(self, AUTH_TOKEN, URL, DEBUG):

    API_URL = f"{URL}/api/portal/savedsearch"

    return _send_request(self, AUTH_TOKEN, "Get saved searches", API_URL, "GET", None, None, DEBUG)