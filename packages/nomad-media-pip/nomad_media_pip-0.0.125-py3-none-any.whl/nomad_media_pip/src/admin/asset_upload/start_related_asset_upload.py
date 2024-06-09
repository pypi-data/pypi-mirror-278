from nomad_media_pip.src.helpers.send_request import _send_request

import os 

def _start_related_asset_upload(self, AUTH_TOKEN, URL, EXISTING_ASSET_ID, RELATED_ASSET_ID, 
                  NEW_RELATED_ASSET_METADATA_TYPE, UPLOAD_OVERWRITE_OPTION, FILE,
                  LANGUAGE_ID, DEBUG):

    API_URL = f"{URL}/api/asset/upload/start-related-asset"
    FILE_STATS = os.stat(FILE)


    FILE_NAME = os.path.basename(FILE)

    AWS_MIN_LIMIT = 5242880
    chunkSize = FILE_STATS.st_size / 10000

    if (chunkSize < (AWS_MIN_LIMIT * 4)):
        chunkSize = 20971520
        
    BODY = {
      	"contentLength":FILE_STATS.st_size,
      	"chunkSize": chunkSize,
        "existingAssetId": EXISTING_ASSET_ID,
        "languageId": LANGUAGE_ID,
        "newRelatedAssetMetadataType": NEW_RELATED_ASSET_METADATA_TYPE,
        "relatedAssetId": RELATED_ASSET_ID,
      	"relativePath": FILE_NAME,
      	"uploadOverwriteOption": UPLOAD_OVERWRITE_OPTION
    }

    return _send_request(self, AUTH_TOKEN, "Start Related Asset Upload", API_URL, "POST", None, BODY, DEBUG)