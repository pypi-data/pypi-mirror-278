from nomad_media_pip.src.helpers.send_request import _send_request

def _remove_input_schedule_event(self, AUTH_TOKEN, URL, CHANNEL_ID, INPUT_ID, DEBUG):
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/liveScheduleEvent/{INPUT_ID}" 

    return _send_request(self, AUTH_TOKEN, "Remove Input Schedule Event", API_URL, "DELETE", None, None, DEBUG)