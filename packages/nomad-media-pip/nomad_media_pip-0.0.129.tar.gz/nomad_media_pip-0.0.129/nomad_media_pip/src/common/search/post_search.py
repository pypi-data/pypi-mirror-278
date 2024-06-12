from nomad_media_pip.src.helpers.send_request import _send_request

def _post_search(self, AUTH_TOKEN, URL, QUERY, OFFSET, SIZE, FILTERS, SORT_FIELDS, SEARCH_RESULT_FIELDS, 
                 FULL_URL_FIELD_NAMES, DISTINCT_ON_FIELD_NAME, INCLUDE_VIDEO_CLIPS, SIMILAR_ASSET_ID,
				 MIN_SCORE, EXCLUDE_TOTAL_RECORD_COUNT, FILTER_BINDER, USE_LLM_SEARCH, 
				 INCLUDE_INTERNAL_FIELDS_IN_RESULTS, IS_ADMIN, DEBUG):
	API_URL = f"{URL}/api/admin/search" if IS_ADMIN else f"{URL}/api/portal/search"

	PARAMS = {
		"includeInternalFieldsInResults": INCLUDE_INTERNAL_FIELDS_IN_RESULTS
	}

	BODY = {
	    "searchQuery": QUERY if QUERY else None,
	    "pageOffset": OFFSET if OFFSET else 0,
	    "pageSize": SIZE if SIZE else 100,
	    "filters": FILTERS if FILTERS else None,
	    "sortFields": SORT_FIELDS if SORT_FIELDS else None,
	    "searchResultFields": SEARCH_RESULT_FIELDS if SEARCH_RESULT_FIELDS else None,
	    "fullUrlFieldNames": FULL_URL_FIELD_NAMES if FULL_URL_FIELD_NAMES else None,
		"distinctOnFieldName": DISTINCT_ON_FIELD_NAME if DISTINCT_ON_FIELD_NAME else None,		
		"includeVideoClips": INCLUDE_VIDEO_CLIPS if INCLUDE_VIDEO_CLIPS != None else None,				
	    "similarAssetId": SIMILAR_ASSET_ID if SIMILAR_ASSET_ID else None,
	    "minScore": MIN_SCORE if MIN_SCORE else None,
	    "excludeTotalRecordCount": EXCLUDE_TOTAL_RECORD_COUNT if EXCLUDE_TOTAL_RECORD_COUNT else None,
	    "filterBinder": FILTER_BINDER if FILTER_BINDER else None,
	    "useLLMSearch": USE_LLM_SEARCH if USE_LLM_SEARCH != None else None
	}

	BODY = {k: v for k, v in BODY.items() if v is not None}

	return _send_request(self, AUTH_TOKEN, "Search", API_URL, "POST", PARAMS, BODY, DEBUG)