from nomad_media_pip.src.helpers.send_request import _send_request

def _add_live_schedule_to_event(self, AUTH_TOKEN, URL, EVENT_ID, SLATE_VIDEO, PREROLL_VIDEO,
                                POSTROLL_VIDEO, IS_SECURE_OUTPUT, ARCHIVE_FOLDER_ASSET,
                                PRIMARY_LIVE_INPUT, BACKUP_LIVE_INPUT, 
                                PRIMARY_LIVESTREAM_INPUT_URL, BACKUP_LIVESTREAM_INPUT_URL, 
                                EXTERNAL_OUTPUT_PROFILES, DEBUG):
    
    API_URL = f"{URL}/api/admin/liveSchedule"
    
    BODY = {
        "contentId": EVENT_ID,
        "slateVideo": SLATE_VIDEO,
        "prerollVideo": PREROLL_VIDEO,
        "postrollVideo": POSTROLL_VIDEO,
        "isSecureOutput": IS_SECURE_OUTPUT,
        "archiveFolderAsset": ARCHIVE_FOLDER_ASSET,
        "primaryLiveInput": PRIMARY_LIVE_INPUT,
        "backupLiveInput": BACKUP_LIVE_INPUT,
        "primaryLivestreamInputUrl": PRIMARY_LIVESTREAM_INPUT_URL,
        "backupLivestreamInputUrl": BACKUP_LIVESTREAM_INPUT_URL,
        "externalOutputProfiles": EXTERNAL_OUTPUT_PROFILES
    }
    
    return _send_request(self, AUTH_TOKEN, "Add Live Schedule To Event", API_URL, "POST", None, BODY, DEBUG) 