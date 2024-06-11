from nomad_media_pip.src.helpers.send_request import _send_request

def _create_playlist(self, AUTH_TOKEN, URL, NAME, THUMBNAIL_ASSET, LOOP_PLAYLIST, DEFAULT_VIDEO_ASSET, DEBUG):

    API_URL = f"{URL}/api/admin/schedule"
       
    BODY = {
        "name": NAME,
        "scheduleType": "1",
        "thumbnailAsset": THUMBNAIL_ASSET,
        "loopPlaylist": LOOP_PLAYLIST,
        "defaultVideoAsset": DEFAULT_VIDEO_ASSET
    }
    
    return _send_request(self, AUTH_TOKEN, "Create Playlist", API_URL, "POST", None, BODY, DEBUG)