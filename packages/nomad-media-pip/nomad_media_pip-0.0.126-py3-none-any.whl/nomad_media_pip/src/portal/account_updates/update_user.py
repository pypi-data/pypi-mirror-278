from nomad_media_pip.src.helpers.send_request import _send_request 
from nomad_media_pip.src.portal.account_updates.get_countries import _get_countries
from nomad_media_pip.src.portal.account_updates.get_states import _get_states
from nomad_media_pip.src.portal.account_updates.get_user import _get_user

def _update_user(self, AUTH_TOKEN, URL, ADDRESS, ADDRESS2, CITY, FIRST_NAME, LAST_NAME, 
        PHONE_NUMBER, PHONE_EXT, POSTAL_CODE, ORGANIZATION, COUNTRY, STATE, DEBUG):

    API_URL = f"{URL}/api/account/user"

    USER_INFO = _get_user(self, AUTH_TOKEN, URL, DEBUG)

    STATE_SELECTED = next((state for state in _get_states(self, AUTH_TOKEN, URL, DEBUG) if state["label"] == STATE), None)
    COUNTRY_SELECTED = next((country for country in _get_countries(self, AUTH_TOKEN, URL, DEBUG) if country["label"] == COUNTRY), None)

    BODY = {
        key: value if value is not None else USER_INFO.get(key)
        for key, value in {
            "address": ADDRESS,
            "address2": ADDRESS2,
            "city": CITY,
            "stateId": STATE_SELECTED,
            "country": COUNTRY_SELECTED,
            "firstName": FIRST_NAME,
            "lastName": LAST_NAME,
            "phone": PHONE_NUMBER,
            "phoneExt": PHONE_EXT,
            "postalCode": POSTAL_CODE,
            "organization": ORGANIZATION,
        }.items()
    }



    return _send_request(self, AUTH_TOKEN, "Update user", API_URL, "PUT", None, BODY, DEBUG)
    