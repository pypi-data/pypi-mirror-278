from nomad_media_pip.src.helpers.send_request import _send_request

import os

def _start_upload(self, AUTH_TOKEN, URL, NAME, EXISTING_ASSET_ID, RELATED_CONTENT_ID, 
                  UPLOAD_OVERWRITE_OPTION, FILE, PARENT_ID, LANGUAGE_ID, DEBUG):

    API_URL = f"{URL}/api/asset/upload/start"
    FILE_STATS = os.stat(FILE)


    FILE_NAME = os.path.basename(FILE)

    CHUNK_SIZE = 8388608

    # Build the payload BODY
    BODY = {
        "displayName": NAME or FILE_NAME,
      	"contentLength":FILE_STATS.st_size,
      	"uploadOverwriteOption": UPLOAD_OVERWRITE_OPTION,
      	"chunkSize": CHUNK_SIZE,
      	"relativePath": FILE_NAME,
        "parentId":	PARENT_ID,
        "existingAssetId": EXISTING_ASSET_ID,
        "relatedContentId": RELATED_CONTENT_ID,
        "languageId": LANGUAGE_ID,
        "uploadOverwriteOption": UPLOAD_OVERWRITE_OPTION
    }

    return _send_request(self, AUTH_TOKEN, "Start Upload", API_URL, "POST", None, BODY, DEBUG)