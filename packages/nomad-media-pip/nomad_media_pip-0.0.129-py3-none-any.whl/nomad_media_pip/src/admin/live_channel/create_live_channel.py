from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.helpers.slugify import _slugify
from nomad_media_pip.src.admin.live_channel.live_channel_types import _LIVE_CHANNEL_TYPES
from nomad_media_pip.src.admin.live_channel.get_security_groups import _get_security_groups

def _create_live_channel(self, AUTH_TOKEN, URL, NAME, THUMBNAIL_IMAGE, ARCHIVE_FOLDER_ASSET, 
                        ENABLE_HIGH_AVAILABILITY, ENABLE_LIVE_CLIPPING, IS_SECURE_OUTPUT, 
                        OUTPUT_SCREENSHOTS, TYPE, EXTERNAL_URL, SECURITY_GROUPS, DEBUG):
    
    API_URL = f"{URL}/api/liveChannel"

    BODY = {
        "name": NAME,
        "routeName": _slugify(NAME),
        "enableHighAvailability": ENABLE_HIGH_AVAILABILITY,
        "enableLiveClipping": ENABLE_LIVE_CLIPPING,
        "isSecureOutput": IS_SECURE_OUTPUT,
        "outputScreenshots": OUTPUT_SCREENSHOTS,
        "type": { "id": _LIVE_CHANNEL_TYPES[TYPE] }
    }

    if THUMBNAIL_IMAGE:
        BODY["thumbnailImage"] = { "id": THUMBNAIL_IMAGE }

    if ARCHIVE_FOLDER_ASSET:
        BODY["archiveFolderAsset"] = { "id": ARCHIVE_FOLDER_ASSET }

    # Set the appropriate fields based on the channel type
    if (TYPE == _LIVE_CHANNEL_TYPES["External"]):
        BODY["externalUrl"] = EXTERNAL_URL

    if SECURITY_GROUPS:
        NOMAD_SECURITY_GROUPS = _get_security_groups(self, AUTH_TOKEN, URL, DEBUG)

        BODY['securityGroups'] = [
        {
            'description': group['description'],
            'id': group['id']
        }
        for group in NOMAD_SECURITY_GROUPS
        if group['description'] in SECURITY_GROUPS
    ]
        
    return _send_request(self, AUTH_TOKEN, "Create Live Channel", API_URL, "POST", None, BODY, DEBUG)