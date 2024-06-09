from nomad_media_pip.src.helpers.send_request import _send_request

def _start_schedule(self, AUTH_TOKEN, URL, ID, SKIP_CLEANUP_ON_FAILURE, DEBUG):

    if SKIP_CLEANUP_ON_FAILURE == None:
        SKIP_CLEANUP_ON_FAILURE = False

    API_URL = f"{URL}/api/admin/schedule/{ID}/start?skipCleanupOnFailure={SKIP_CLEANUP_ON_FAILURE}"

    return _send_request(self, AUTH_TOKEN, "Start Schedule", API_URL, "POST", None, None, DEBUG)