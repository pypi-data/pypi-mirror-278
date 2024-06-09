from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.schedule.get_playlist import _get_playlist

def _update_playlist(self, AUTH_TOKEN, URL, ID, DEFAULT_VIDEO_ASSET, LOOP_PLAYLIST, NAME,
                     THUMBNAIL_ASSET, DEBUG):
        
    API_URL = f"{URL}/api/admin/schedule/{ID}"

    PLAYLIST = _get_playlist(self, AUTH_TOKEN, URL, ID, DEBUG)
       
    BODY = {
        "defaultVideoAsset": DEFAULT_VIDEO_ASSET or PLAYLIST.get("defaultVideoAsset"),
        "id": ID,
        "loopPlaylist": LOOP_PLAYLIST or PLAYLIST.get("loopPlaylist"),
        "name": NAME or PLAYLIST.get("name"),
        "scheduleType": "1",
        "thumbnailAsset": THUMBNAIL_ASSET or PLAYLIST.get("thumbnailAsset")
    }

    return _send_request(self, AUTH_TOKEN, "Update Playlist", API_URL, "PUT", None, BODY, DEBUG)