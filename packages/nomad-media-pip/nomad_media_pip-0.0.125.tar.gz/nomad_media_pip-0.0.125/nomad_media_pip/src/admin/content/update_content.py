from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.content.get_content import _get_content

from deepdiff import DeepDiff

def _update_content(self, AUTH_TOKEN, URL, ID, CONTENT_DEFINITION_ID, PROPERTIES, 
                    LANGUAGE_ID, DEBUG):
    API_URL = f"{URL}/api/content/{ID}"
    
    try:
        BODY = _get_content(self, AUTH_TOKEN, URL, ID, CONTENT_DEFINITION_ID, None, DEBUG)

        if (BODY["contentDefinitionId"] != CONTENT_DEFINITION_ID): BODY["contentDefinitionId"] = CONTENT_DEFINITION_ID
        if (BODY.get("languageId") != LANGUAGE_ID): BODY["languageId"] = LANGUAGE_ID
        if (BODY["contentId"] != ID): BODY["contentId"] = ID

        _update_properties(BODY, PROPERTIES)

    except:
        BODY = {
            "contentDefinitionId": CONTENT_DEFINITION_ID,
            "contentId": ID,
            "languageId": LANGUAGE_ID,
            "properties": PROPERTIES
        }

    return _send_request(self, AUTH_TOKEN, "Update content", API_URL, "PUT", None, BODY, DEBUG)

def _update_properties(body, properties):
    for property, value in properties.items():
        if isinstance(value, list):
            for i in range(len(value)):
                if DeepDiff(body['properties'][property][i], value[i]):
                    body['properties'][property][i] = value[i]
        elif isinstance(value, dict):
            if DeepDiff(body['properties'][property], value):
                body['properties'][property] = value
        elif body['properties'].get(property) != value:
            body['properties'][property] = value

