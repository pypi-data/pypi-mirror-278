from nomad_media_pip.src.admin.asset_upload.upload_asset_part import _upload_asset_part
from nomad_media_pip.src.admin.asset_upload.upload_asset_part_complete import _upload_asset_part_complete

def _upload_thread(self, AUTH_TOKEN, URL, FILE, PART, worker_count, DEBUG):
    ETAG = _upload_asset_part(FILE, PART, DEBUG)
    _upload_asset_part_complete(self, AUTH_TOKEN, URL, PART["id"], ETAG, DEBUG)

    worker_count["value"] -= 1
