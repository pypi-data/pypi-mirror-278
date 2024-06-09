from nomad_media_pip.src.helpers.send_request import _send_request

def _clip_asset(self, AUTH_TOKEN, URL, ASSET_ID, ASSET_TYPE, START_TIME_CODE, END_TIME_CODE, 
                TITLE, OUTPUT_FOLDER_ID, TAGS, COLLECTIONS, RELATED_CONTENTS, VIDEO_BITRATE, 
                AUDIO_TRACKS, DEBUG):
    
    API_URL = f"{URL}/api/admin/asset/{ASSET_ID}/clip" if ASSET_TYPE == "admin" else f"{URL}/api/asset/{ASSET_ID}/clip"

    BODY = {
        "startTimecode": START_TIME_CODE,
        "endTimecode": END_TIME_CODE,
        "title": TITLE,
        "outputFolderId": OUTPUT_FOLDER_ID,
        "tags": TAGS,
        "collections": COLLECTIONS,
        "relatedContent": RELATED_CONTENTS,
        "videoBitrate": VIDEO_BITRATE,
        "audioTracks": AUDIO_TRACKS
    }

    return _send_request(self, AUTH_TOKEN, "Clip asset", API_URL, "POST", None, BODY, DEBUG)