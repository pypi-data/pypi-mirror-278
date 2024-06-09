from nomad_media_pip.src.helpers.send_request import _send_request 

def _move_asset(self, AUTH_TOKEN, URL, ASSET_ID, DESTINATION_FOLDER_ID, NAME, BATCH_ACTION,
                CONTENT_DEFINITION_ID, SCHEMA_NAME, USER_ID, RESOLVER_EXCEMPT, DEBUG):
    
    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/move"

    BODY = {
        "actionArguments": {
            "destinationFolderAssetId": DESTINATION_FOLDER_ID
        },
        "targetIds": [ASSET_ID],
        "batchAction": BATCH_ACTION,
        "contentDefinitionId": CONTENT_DEFINITION_ID,
        "schemaName": SCHEMA_NAME,
        "userId": USER_ID,
        "resolverExempt": RESOLVER_EXCEMPT
    }

    if NAME is not None:
        BODY["actionArguments"]["name"] = NAME

    return _send_request(self, AUTH_TOKEN, "Move asset", API_URL, "POST", None, BODY, DEBUG)
    