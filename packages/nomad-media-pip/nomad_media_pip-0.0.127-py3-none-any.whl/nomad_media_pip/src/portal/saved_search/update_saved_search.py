from nomad_media_pip.src.helpers.send_request import _send_request 

from nomad_media_pip.src.portal.saved_search.get_saved_search import _get_saved_search

def _update_saved_search(self, AUTH_TOKEN, URL, ID, NAME, FEATURED, BOOKMARKED, PUBLIC, SEQUENCE, 
                         TYPE, QUERY, OFFSET, SIZE, FILTERS, SORT_FIELDS, 
                         SEARCH_RESULT_FIELDS, SIMILAR_ASSET_ID, MIN_SCORE, 
                         EXCLUDE_TOTAL_RECORD_COUNT, FILTER_BINDER, DEBUG):
    
    API_URL = f"{URL}/api/portal/savedsearch/{ID}"

    SAVED_SEARCH_INFO = _get_saved_search(self, AUTH_TOKEN, URL, ID, DEBUG)

    BODY = {
        key: value for key, value in {
            "id": ID,
            "name": NAME or SAVED_SEARCH_INFO.get("name"),
            "featured": FEATURED or SAVED_SEARCH_INFO.get("featured"),
            "bookmarked": BOOKMARKED or SAVED_SEARCH_INFO.get("bookmarked"),
            "public": PUBLIC or SAVED_SEARCH_INFO.get("public"),
            "pageSize": SIZE or SAVED_SEARCH_INFO.get("pageSize"),
            "sequence": SEQUENCE or SAVED_SEARCH_INFO.get("sequence"),
            "type": TYPE or SAVED_SEARCH_INFO.get("type"),
            "user": SAVED_SEARCH_INFO.get("user"),
            "criteria": {
                key : value for key, value in {
                    "query": QUERY or SAVED_SEARCH_INFO.get("criteria").get("query"),
                    "pageOffset": OFFSET or SAVED_SEARCH_INFO.get("criteria").get("pageOffset"),
                    "pageSize": SIZE or SAVED_SEARCH_INFO.get("criteria").get("pageSize"),
                    "filters": FILTERS or SAVED_SEARCH_INFO.get("criteria").get("filters"),
                    "sortFields": SORT_FIELDS or SAVED_SEARCH_INFO.get("criteria").get("sortFields"),
                    "searchResultFields": SEARCH_RESULT_FIELDS or SAVED_SEARCH_INFO.get("criteria").get("searchResultFields"),
                    "similarAssetId": SIMILAR_ASSET_ID or SAVED_SEARCH_INFO.get("criteria").get("similarAssetId"),
                    "minScore": MIN_SCORE or SAVED_SEARCH_INFO.get("criteria").get("minScore"),
                    "excludeTotalRecordCount": EXCLUDE_TOTAL_RECORD_COUNT or SAVED_SEARCH_INFO.get("criteria").get("excludeTotalRecordCount"),
                    "filterBinder": FILTER_BINDER or SAVED_SEARCH_INFO.get("criteria").get("filterBinder")
                }.items() if value is not None
            }
        }.items() if value is not None
    }

    return _send_request(self, AUTH_TOKEN, "Update saved search", API_URL, "PUT", None, BODY, DEBUG)
    