from nomad_media_pip.src.helpers.send_request import _send_request

def _clear_watchlist(self, AUTH_TOKEN, URL, USER_ID, DEBUG):

    API_URL = f"{URL}/api/media/clear-watching?userId={USER_ID}"

    return _send_request(self, AUTH_TOKEN, "Clear Watchlist", API_URL, "POST", None, None, DEBUG)