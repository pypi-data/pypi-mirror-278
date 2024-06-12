from nomad_media_pip.src.helpers.send_request import _send_request

def _stop_schedule(self, AUTH_TOKEN, URL, ID, FORCE_STOP, DEBUG):
    if FORCE_STOP == None:
        FORCE_STOP = False

    API_URL = f"{URL}/api/admin/schedule/{ID}/stop?force={FORCE_STOP}"

    return _send_request(self, AUTH_TOKEN, "Stop Schedule", API_URL, "POST", None, None, DEBUG)