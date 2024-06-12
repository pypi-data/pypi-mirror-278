from nomad_media_pip.src.helpers.send_request import _send_request

def _publish_intelligent_schedule(self, AUTH_TOKEN, URL, SCHEDULE_ID, NUMBER_OR_LOCKED_DAYS, DEBUG):

    API_URL = f"{URL}/api/admin/schedule/{SCHEDULE_ID}/publish"
    
    BODY = {
        "number_of_days": NUMBER_OR_LOCKED_DAYS
    }

    return _send_request(self, AUTH_TOKEN, "Publish Intelligent Schedule", API_URL, "POST", None, BODY, DEBUG)