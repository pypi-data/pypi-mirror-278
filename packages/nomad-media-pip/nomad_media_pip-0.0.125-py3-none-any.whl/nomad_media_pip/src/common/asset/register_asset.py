from nomad_media_pip.src.helpers.send_request import _send_request 

def _register_asset(self, AUTH_TOKEN, URL, ASSET_ID, PARENT_ID, DISPLAY_OBJECT_KEY, BUCKET_NAME,
                    OBJECT_KEY, ETAG, TAGS, COLLECTIONS, RELATED_CONTENTS, SEQUENCER,
                    ASSET_STATUS, STORAGE_CLASS, ASSET_TYPE, CONTENT_LENGTH, STORAGE_EVENT_NAME,
                    CREATED_DATE, STORAGE_SOURCE_IP_ADDRESS, START_MEDIA_PROCESSOR,
                    DELETE_MISSING_ASSET, DEBUG):
    
    API_URL = f"{URL}/api/admin/asset/register"

    BODY = {
        "id": ASSET_ID,
        "parentId": PARENT_ID,
        "displayObjectKey": DISPLAY_OBJECT_KEY,
        "bucketName": BUCKET_NAME,
        "objectKey": OBJECT_KEY,
        "eTag": ETAG,
        "tags": TAGS,
        "collections": COLLECTIONS,
        "relatedContents": RELATED_CONTENTS,
        "sequencer": SEQUENCER,
        "assetStatus": ASSET_STATUS,
        "storageClass": STORAGE_CLASS,
        "assetType": ASSET_TYPE,
        "contentLength": CONTENT_LENGTH,
        "storageEventName": STORAGE_EVENT_NAME,
        "createdDate": CREATED_DATE,
        "storageSourceIpAddress": STORAGE_SOURCE_IP_ADDRESS,
        "startMediaProcessor": START_MEDIA_PROCESSOR,
        "deleteMissingAsset": DELETE_MISSING_ASSET
    }

    return _send_request(self, AUTH_TOKEN, "Register asset", API_URL, "POST", None, BODY, DEBUG)
    