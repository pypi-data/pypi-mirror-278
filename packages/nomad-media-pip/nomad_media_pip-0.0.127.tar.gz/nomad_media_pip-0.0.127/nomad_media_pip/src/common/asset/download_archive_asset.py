from nomad_media_pip.src.helpers.send_request import _send_request 

def _download_archive_asset(self, AUTH_TOKEN, URL, API_TYPE, ASSET_IDS, FILE_NAME, DOWNLOAD_PROXY,
                            DEBUG):
    
    API_URL = f"{URL}/api/admin/asset/download-archive" if API_TYPE == "admin" else f"{URL}/api/asset/download-archive"

    BODY = {
        "assetIds": ASSET_IDS
    }

    if API_TYPE == "admin":
        BODY["fileName"] = FILE_NAME
        BODY["downloadProxy"] = DOWNLOAD_PROXY

    return _send_request(self, AUTH_TOKEN, "Download archive asset", API_URL, "POST", None, BODY, DEBUG)
    