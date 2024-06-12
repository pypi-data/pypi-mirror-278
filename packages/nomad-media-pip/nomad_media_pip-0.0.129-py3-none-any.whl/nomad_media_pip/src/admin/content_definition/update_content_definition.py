from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.content_definition.get_content_definition import _get_content_definition
from nomad_media_pip.src.admin.content_definition.get_content_definition_groups import _get_content_definition_groups
from nomad_media_pip.src.admin.content_definition.get_content_definition_types import _get_content_definition_types
from nomad_media_pip.src.admin.live_channel.get_security_groups import _get_security_groups
from nomad_media_pip.src.admin.content_definition.get_system_roles import _get_system_roles

def _update_content_definition(self, AUTH_TOKEN, URL, ID, NAME, CONTENT_FIELDS, CONTENT_DEFINITION_GROUP, 
                               CONTENT_DEFINITION_TYPE, DISPLAY_FIELD, ROUTE_ITEM_NAME_FIELD, SECURITY_GROUPS, 
                               SYSTEM_ROLES, INCLUDE_IN_TAGS, INDEX_CONTENT, DEBUG):

    API_URL = f"{URL}/api/contentDefinition/{ID}"

    if CONTENT_DEFINITION_GROUP:
        CONTENT_DEFINIITON_GROUPS = _get_content_definition_groups(self, AUTH_TOKEN, URL, DEBUG)
        CONTENT_DEFINITION_GROUP_INFO = next((group for group in CONTENT_DEFINIITON_GROUPS["items"] if group["title"] == CONTENT_DEFINITION_GROUP), None)
    else:
        CONTENT_DEFINITION_GROUP_INFO = None

    if CONTENT_DEFINITION_TYPE:
        CONTENT_DEFINITION_TYPES = _get_content_definition_types(self, AUTH_TOKEN, URL, DEBUG)
        CONTENT_DEFINITION_TYPE_INFO = next((type for type in CONTENT_DEFINITION_TYPES["items"] if type["description"] == CONTENT_DEFINITION_TYPE), None)
    else:
        CONTENT_DEFINITION_TYPE_INFO = None

    try:
        CONTENT_DEFINITION_INFO = _get_content_definition(self, AUTH_TOKEN, URL, ID, DEBUG)
        if DISPLAY_FIELD: DISPLAY_FIELD_INFO = next((field for field in CONTENT_DEFINITION_INFO["contentFields"] if field["properties"]["title"] == DISPLAY_FIELD), None)
        if ROUTE_ITEM_NAME_FIELD: ROUTE_ITEM_NAME_FIELD_INFO = next((field for field in CONTENT_DEFINITION_INFO["contentFields"] if field["properties"]["title"] == ROUTE_ITEM_NAME_FIELD), None)
    except:
        CONTENT_DEFINITION_INFO = None
        DISPLAY_FIELD_INFO = next((field for field in CONTENT_FIELDS if field["properties"]["title"] == DISPLAY_FIELD), None) if DISPLAY_FIELD else None
        ROUTE_ITEM_NAME_FIELD_INFO = next((field for field in CONTENT_FIELDS if field["properties"]["title"] == ROUTE_ITEM_NAME_FIELD), None) if ROUTE_ITEM_NAME_FIELD else None

    if SECURITY_GROUPS:
        SECURITY_GROUPS_INFO = _get_security_groups(self, AUTH_TOKEN, URL, DEBUG)
        SECURITY_GROUPS_SELECTED_INFO = [group for group in SECURITY_GROUPS_INFO["items"] if group["description"] in SECURITY_GROUPS]
    else:
        SECURITY_GROUPS_SELECTED_INFO = None

    if SYSTEM_ROLES:
        SYSTEM_ROLES_INFO = _get_system_roles(self, AUTH_TOKEN, URL, DEBUG)
        SYSTEM_ROLES_SELECTED_INFO = [role for role in SYSTEM_ROLES_INFO["items"] if role["description"] in SYSTEM_ROLES]
    else:
        SYSTEM_ROLES_SELECTED_INFO = None

    BODY = {
        "contentDefinitionId": ID,
        "contentFields": CONTENT_FIELDS or CONTENT_DEFINITION_INFO.get("contentFields"),
        "properties": {
            "assignedSecurityGroups": SECURITY_GROUPS_SELECTED_INFO if SECURITY_GROUPS_SELECTED_INFO is not None else CONTENT_DEFINITION_INFO.get("assignedSecurityGroups") if CONTENT_DEFINITION_INFO is not None else [],
            "assignedSystemRoles": SYSTEM_ROLES_SELECTED_INFO if SYSTEM_ROLES_SELECTED_INFO is not None else CONTENT_DEFINITION_INFO.get("assignedSystemRoles") if CONTENT_DEFINITION_INFO is not None else [],
            "includeInTags": INCLUDE_IN_TAGS if INCLUDE_IN_TAGS is not None else CONTENT_DEFINITION_INFO.get("includeTags") if CONTENT_DEFINITION_INFO is not None else None,
            "indexContent": INDEX_CONTENT if INDEX_CONTENT is not None else CONTENT_DEFINITION_INFO.get("indexContent") if CONTENT_DEFINITION_INFO is not None else None,
            "title": NAME if NAME is not None else CONTENT_DEFINITION_INFO.get("title") if CONTENT_DEFINITION_INFO is not None else None
        }
    }
    
    BODY["properties"]["contentDefinitionGroupId"] = { "description": CONTENT_DEFINITION_GROUP_INFO["title"], "id": CONTENT_DEFINITION_GROUP_INFO["contentDefinitionGroupId"] } if CONTENT_DEFINITION_GROUP_INFO is not None else CONTENT_DEFINITION_INFO.get("contentDefinitionGroupId") if CONTENT_DEFINITION_INFO is not None else None
    BODY["properties"]["contentTypeId"] = { "description": CONTENT_DEFINITION_TYPE_INFO["description"], "id": CONTENT_DEFINITION_TYPE_INFO["id"] } if CONTENT_DEFINITION_TYPE_INFO is not None else CONTENT_DEFINITION_INFO.get("contentDefinitionTypeId") if CONTENT_DEFINITION_INFO is not None else None
    BODY["properties"]["displayField"] = { "description": DISPLAY_FIELD_INFO["properties"]["title"], "id": DISPLAY_FIELD_INFO["contentFieldId"] } if DISPLAY_FIELD_INFO is not None else CONTENT_DEFINITION_INFO.get("displayField") if CONTENT_DEFINITION_INFO is not None else None
    BODY["properties"]["routeItemNameField"] = { "description": ROUTE_ITEM_NAME_FIELD_INFO["properties"]["title"], "id": ROUTE_ITEM_NAME_FIELD_INFO["id"] } if ROUTE_ITEM_NAME_FIELD_INFO is not None else CONTENT_DEFINITION_INFO.get("routeItemNameField") if CONTENT_DEFINITION_INFO is not None else None

    return _send_request(self, AUTH_TOKEN, "Update content definition", API_URL, "PUT", None, BODY, DEBUG)