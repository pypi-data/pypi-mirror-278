from nomad_media_pip.src.helpers.send_request import _send_request 
from nomad_media_pip.src.common.asset.get_asset_details import _get_asset_details

def _bulk_update_metadata(self, AUTH_TOKEN, URL, CONTENT_IDS, COLLECTION_IDS, RELATED_CONTENT_IDS, 
                          TAG_IDS, SCHEMA_NAME, DEBUG):
    
    API_URL = f"{URL}/api/admin/content/bulk-metadata-update"

    ASSET_DETAILS =  _get_asset_details(self, AUTH_TOKEN, URL, CONTENT_IDS[0], "admin", DEBUG)

    BODY = {
        'collections': (COLLECTION_IDS if COLLECTION_IDS else []) + 
                       ([item['id'] for item in ASSET_DETAILS['collections']] if 'collections' in ASSET_DETAILS and ASSET_DETAILS['collections'] else []),
        'contents': CONTENT_IDS,
        'relatedContents': (RELATED_CONTENT_IDS if RELATED_CONTENT_IDS else []) + 
                           ([item['id'] for item in ASSET_DETAILS['relatedContents']] if 'relatedContents' in ASSET_DETAILS and ASSET_DETAILS['relatedContents'] else []),
        'tags': (TAG_IDS if TAG_IDS else []) + 
                 ([item['id'] for item in ASSET_DETAILS['tags']] if 'tags' in ASSET_DETAILS and ASSET_DETAILS['tags'] else []),
        'schemaName': SCHEMA_NAME
    }

    return _send_request(self, AUTH_TOKEN, "Bulk update metadata", API_URL, "POST", None, BODY, DEBUG)
    