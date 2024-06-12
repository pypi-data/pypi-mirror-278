from nomad_media_pip.src.helpers.send_request import _send_request

import time

def _extend_live_schedule(self, AUTH_TOKEN, URL, EVENT_ID, RECURRING_DAYS, RECURRING_WEEKS,
                          END_DATE, DEBUG):
    
    API_URL = f"{URL}/api/admin/liveSchedule/content/{EVENT_ID}/copy"

    BODY = {
        "recurringDays": RECURRING_DAYS,
        "recurringWeeks": RECURRING_WEEKS,
        "endDate": END_DATE,
        "timeZoneOffsetSeconds": -time.timezone
    }

    return _send_request(self, AUTH_TOKEN, "Extend Live Schedule", API_URL, "POST", None, BODY, DEBUG) 