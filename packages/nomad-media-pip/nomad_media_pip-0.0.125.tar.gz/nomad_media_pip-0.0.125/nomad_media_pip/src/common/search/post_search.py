from nomad_media_pip.src.helpers.send_request import _send_request

def _post_search(self, AUTH_TOKEN, URL, QUERY, OFFSET, SIZE, FILTERS, SORT_FIELDS, RESULT_FIELDS, 
                 SIMILAR_ASSET_ID, MIN_SCORE, EXCLUDE_TOTAL_RECORD_COUNT, FILTER_BINDER, 
				 IS_ADMIN, DEBUG):
	API_URL = f"{URL}/api/admin/search" if IS_ADMIN else f"{URL}/api/portal/search"

	BODY = {}

	if QUERY: BODY["searchQuery"] = QUERY 
	BODY["pageOffset"] = OFFSET if OFFSET else 0
	BODY["pageSize"] = SIZE if SIZE else 100
	if FILTERS: BODY["filters"] = FILTERS
	if SORT_FIELDS: BODY["sortFields"] = SORT_FIELDS
	if RESULT_FIELDS: BODY["resultFields"] = RESULT_FIELDS
	if SIMILAR_ASSET_ID: BODY["similarAssetId"] = SIMILAR_ASSET_ID
	if MIN_SCORE: BODY["minScore"] = MIN_SCORE
	if EXCLUDE_TOTAL_RECORD_COUNT: BODY["excludeTotalRecordCount"] = EXCLUDE_TOTAL_RECORD_COUNT
	if FILTER_BINDER: BODY["filterBinder"] = FILTER_BINDER

	return _send_request(self, AUTH_TOKEN, "Search", API_URL, "POST", None, BODY, DEBUG)