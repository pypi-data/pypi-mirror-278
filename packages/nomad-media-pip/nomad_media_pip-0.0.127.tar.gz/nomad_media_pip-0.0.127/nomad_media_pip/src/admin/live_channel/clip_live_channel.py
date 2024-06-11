from nomad_media_pip.src.helpers.send_request import _send_request

def _clip_live_channel(self, AUTH_TOKEN, URL, CHANNEL_ID, START_TIME_CODE, END_TIME_CODE, TITLE, 
                       OUTPUT_FOLDER_ID, TAGS, COLLECTIONS, RELATED_CONTENTS, VIDEO_BITRATE, 
                       AUDIO_TRACKS, DEBUG):
        
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/clip"
    
    BODY = {
        "startTimeCode": START_TIME_CODE,
        "endTimeCode": END_TIME_CODE,
        "title": TITLE,
        "outputFolderId": OUTPUT_FOLDER_ID,
        "tags": TAGS,
        "collections": COLLECTIONS,
        "relatedContent": RELATED_CONTENTS,
        "videoBitrate": VIDEO_BITRATE,
        "audioTracks": AUDIO_TRACKS
    }
    
    _send_request(self, AUTH_TOKEN, "Clip Live Channel", API_URL, "POST", None, BODY, DEBUG) 
