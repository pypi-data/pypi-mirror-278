from nomad_media_pip.src.helpers.send_request import _send_request 

def _add_saved_search(self, AUTH_TOKEN, URL, NAME, FEATURED, BOOKMARKED, PUBLIC, SEQUENCE, TYPE,
                      QUERY, OFFSET, SIZE, FILTERS, SORT_FIELDS, SEARCH_RESULT_FIELDS,
                      SIMILAR_ASSET_ID, MIN_SCORE, EXCLUDE_TOTAL_RECORD_COUNT, FILTER_BINDER,
                      DEBUG):
    
    API_URL = f"{URL}/api/portal/savedsearch"

    BODY = {
        "name": NAME,
        "featured": FEATURED,
        "bookmarked": BOOKMARKED,
        "public": PUBLIC,
        "pageSize": SIZE,
        "sequence": SEQUENCE,
        "type": TYPE,
        "criteria": {}
    }

    if QUERY: BODY["criteria"]["query"] = QUERY
    BODY["criteria"]["pageOffset"] = OFFSET if OFFSET else 0
    BODY["criteria"]["pageSize"] = SIZE if SIZE else 10
    if FILTERS: BODY["criteria"]["filters"] = FILTERS
    if SORT_FIELDS: BODY["criteria"]["sortFields"] = SORT_FIELDS
    if SEARCH_RESULT_FIELDS: BODY["criteria"]["searchResultFields"] = SEARCH_RESULT_FIELDS
    if SIMILAR_ASSET_ID: BODY["criteria"]["similarAssetId"] = SIMILAR_ASSET_ID
    if MIN_SCORE: BODY["criteria"]["minScore"] = MIN_SCORE
    if EXCLUDE_TOTAL_RECORD_COUNT: BODY["criteria"]["excludeTotalRecordCount"] = EXCLUDE_TOTAL_RECORD_COUNT
    if FILTER_BINDER: BODY["criteria"]["filterBinder"] = FILTER_BINDER

    return _send_request(self, AUTH_TOKEN, "Add saved search", API_URL, "POST", None, BODY, DEBUG)
    