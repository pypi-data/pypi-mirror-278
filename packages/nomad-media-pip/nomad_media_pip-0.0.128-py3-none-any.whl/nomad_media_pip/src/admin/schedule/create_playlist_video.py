from nomad_media_pip.src.helpers.send_request import _send_request

def _create_playlist_video(self, AUTH_TOKEN, URL, PLAYLIST_ID, ASSET, PREVIOUS_ITEM, DEBUG):
    
    API_URL = f"{URL}/api/admin/schedule/{PLAYLIST_ID}/item"
       
    BODY = {
        "asset": ASSET,
        "previousItem": PREVIOUS_ITEM
    }
    
    return _send_request(self, AUTH_TOKEN, "Create Playlist Video", API_URL, "POST", None, BODY, DEBUG)