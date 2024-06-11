from nomad_media_pip.src.helpers.send_request import _send_request

def _get_live_channel_schedule_events(self, AUTH_TOKEN, URL, CHANNEL_ID, DEBUG):
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/liveScheduleEvent"

    return _send_request(self, AUTH_TOKEN, "Get Live Channel Schedule Events", API_URL, "GET", None, None, DEBUG)