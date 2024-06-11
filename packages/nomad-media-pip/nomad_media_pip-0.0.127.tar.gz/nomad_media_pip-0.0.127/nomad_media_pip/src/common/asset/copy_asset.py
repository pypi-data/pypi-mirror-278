from nomad_media_pip.src.helpers.send_request import _send_request 

def _copy_asset(self, AUTH_TOKEN, URL, ASSET_IDS, DESTINATION_FOLDER_ID,
                BATCH_ACTION, CONTENT_DEFINITION_ID, SCHEMA_NAME, RESOLVER_EXCEMPT,
                USER_ID, DEBUG):

    API_URL = f"{URL}/api/admin/asset//copy"

    BODY = {
        "batchAction": BATCH_ACTION,
        "contentDefinitionId": CONTENT_DEFINITION_ID,
        "schemaName": SCHEMA_NAME,
        "targetIds": ASSET_IDS,
        "userId": USER_ID,
        "actionArguments": {
            "destinationFolderAssetId": DESTINATION_FOLDER_ID
        },
        "resolverExempt": RESOLVER_EXCEMPT
    }

    return _send_request(self, AUTH_TOKEN, "Copy asset", API_URL, "POST", None, BODY, DEBUG)
    