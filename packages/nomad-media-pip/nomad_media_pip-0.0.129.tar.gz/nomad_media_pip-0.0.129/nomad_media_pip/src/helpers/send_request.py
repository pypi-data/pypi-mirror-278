from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import json, requests, time
MAX_RETRIES = 5
TIMEOUT = 30
SLEEP_TIME = 60

def _send_request(self, AUTH_TOKEN, FUNCTION_NAME, URL, METHOD_TYPE, PARAMS, BODY, DEBUG):
    
    HEADERS = {
        "Content-Type": "application/json"
    }

    if AUTH_TOKEN: HEADERS["Authorization"] = f"Bearer {AUTH_TOKEN}"

    if DEBUG: print(f"URL: {URL}\nMETHOD: {METHOD_TYPE}" + (f"\nPARAMS: {json.dumps(PARAMS, indent=4)}" if PARAMS else "")  + (f"\nBODY: {json.dumps(BODY, indent=4) }" if BODY else ""))

    retries = 0
    while True:
        try:
            RESPONSE = requests.request(METHOD_TYPE, URL, headers = HEADERS, params=PARAMS if PARAMS else None, data = json.dumps(BODY) if BODY else None, timeout = TIMEOUT)

            if RESPONSE.ok:
                break

            if RESPONSE.status_code == 403 and FUNCTION_NAME != "Refresh Token":
                self.refresh_token()
                time.sleep(SLEEP_TIME * 2 ** retries)
            else:
                raise Exception()
            
        except requests.exceptions.Timeout:
            if retries < MAX_RETRIES:
                retries += 1
                time.sleep(SLEEP_TIME * 2 ** retries)
        
        except Exception as e:
            _api_exception_handler(RESPONSE, f"{FUNCTION_NAME} failed: {e}")

    try: return RESPONSE.json() 
    except: return