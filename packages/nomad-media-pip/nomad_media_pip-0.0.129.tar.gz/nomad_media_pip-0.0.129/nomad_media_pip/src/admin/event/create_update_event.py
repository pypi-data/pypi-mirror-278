from nomad_media_pip.src.helpers.send_request import _send_request

def _create_and_update_event(self, AUTH_TOKEN, URL, CONTENT_ID, CONTENT_DEFINITION_ID, 
                             NAME, START_DATETIME, END_DATETIME, EVENT_TYPE, SERIES,
                             DISABLED, OVERRIED_SERIES_PROPERTIES, SERIES_PROPERTIES, DEBUG):
    
    if (CONTENT_ID == "" or CONTENT_ID == None):
        API_URL = f"{URL}/api/content/new?contentDefinitionId={CONTENT_DEFINITION_ID}"

    INFO = _send_request(self, AUTH_TOKEN, "Create Event", API_URL, "GET", None, None, DEBUG) 
    CONTENT_ID = INFO["contentId"]

    API_URL = f"{URL}/api/content/{CONTENT_ID}"

    if not SERIES_PROPERTIES or not OVERRIED_SERIES_PROPERTIES: SERIES_PROPERTIES = {}

    SERIES_PROPERTIES["name"] = NAME if NAME else SERIES["description"]
    SERIES_PROPERTIES["startDateTime"] = START_DATETIME
    SERIES_PROPERTIES["endDateTime"] = END_DATETIME
    SERIES_PROPERTIES["eventType"] = EVENT_TYPE
    if SERIES: SERIES_PROPERTIES["series"] = SERIES
    SERIES_PROPERTIES["disabled"] = DISABLED
    SERIES_PROPERTIES["overrideSeriesDetails"] = OVERRIED_SERIES_PROPERTIES

    BODY = {
        "contentId": CONTENT_ID,
        "contentDefinitionId": CONTENT_DEFINITION_ID,
        "properties": SERIES_PROPERTIES
    }

    return _send_request(self, AUTH_TOKEN, "Update Event", API_URL, "PUT", None, BODY, DEBUG) 