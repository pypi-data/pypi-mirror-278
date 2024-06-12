from nomad_media_pip.src.helpers.send_request import _send_request

def _get_user_uploads(self, AUTH_TOKEN, URL, INCLUDE_COMPLETED_UPLOADS, DEBUG):

    API_URL = f"{URL}/api/admin/asset/upload?includeCompletedUploads={INCLUDE_COMPLETED_UPLOADS}"

    return _send_request(self, AUTH_TOKEN, "Get user uploads", API_URL, "GET", None, None, DEBUG)