from nomad_media_pip.src.helpers.send_request import _send_request

import re

def _get_states(self, AUTH_TOKEN, URL, DEBUG):
    EDITED_URL = re.sub(r'https://(.+?)\.', 'https://', URL)
    EDITED_URL = EDITED_URL[:EDITED_URL.rfind('/')]
    API_URL = f"{EDITED_URL}/config/ea1d7060-6291-46b8-9468-135e7b94021b/lookups.json"
 
    return _send_request(self, AUTH_TOKEN, "Get countries", API_URL, "GET", None, None, DEBUG)