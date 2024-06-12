from nomad_media_pip.src.helpers.send_request import _send_request 

def _start_workflow(self, AUTH_TOKEN, URL, ACTION_ARGUMENTS, TARGET_IDS, DEBUG):

    API_URL = f"{URL}/api/admin/asset/startWorkflow"

    BODY = {
        "actionArguments": ACTION_ARGUMENTS,
        "targetIds": TARGET_IDS
    }

    return _send_request(self, AUTH_TOKEN, "Start workflow", API_URL, "POST", None, BODY, DEBUG)
    