from nomad_media_pip.src.helpers.send_request import _send_request

def _update_playlist_video(self, AUTH_TOKEN, URL, SCHEDULE_ID, ITEM_ID, ASSET, DEBUG):

    API_URL = f"{URL}/api/admin/schedule/{SCHEDULE_ID}/item/{ITEM_ID}"
    
    BODY = {
        "asset": ASSET
    }

    return _send_request(self, AUTH_TOKEN, "Update Playlist Video", API_URL, "PUT\nBODY: {json.dumps(BODY", None, BODY, DEBUG)