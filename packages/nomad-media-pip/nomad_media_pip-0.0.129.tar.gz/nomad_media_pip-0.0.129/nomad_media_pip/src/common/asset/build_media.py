from nomad_media_pip.src.helpers.send_request import _send_request

def _build_media(self, AUTH_TOKEN, URL, SOURCE, TITLE, TAGS, COLLECTIONS, RELATED_CONTENT,
                 DESTINATION_FOLDER_ID, VIDEO_BITRATE, AUDIO_TRACKS, DEBUG):
    
    API_URL = f"{URL}/api/asset/build-media"

    BODY = {
        "source": SOURCE,
        "title": TITLE,
        "destinationFolderId": DESTINATION_FOLDER_ID,
        "tags": TAGS,
        "collections": COLLECTIONS,
        "relatedContent": RELATED_CONTENT,
        "videoBitrate": VIDEO_BITRATE,
        "audioTracks": AUDIO_TRACKS
    }

    return _send_request(self, AUTH_TOKEN, "Build media", API_URL, "POST", None, BODY, DEBUG)    