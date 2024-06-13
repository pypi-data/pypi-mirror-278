from typing import Dict, List, Union, Optional

from dooray_api_wrapper.common import dooray_request
from dooray_api_wrapper.const.const import Scope, Type, State
from dooray_api_wrapper.structure import response_result, response_header


def get_wiki_list(page: int = 0, size: int = 0) -> Optional[response_result.WikiResult]:
    """접근 가능한 위키 목록을 조회합니다."""
    end_point = f"/wiki/v1/wikis"
    params = {
        "page": page,
        "size": size,
    }
    response = dooray_request.dooray_get(end_point, params)
    if response is None:
        return None

    header = response["header"]
    result = {"result": response["result"]}
    return response_result.WikiResult(**result)


def get_wiki_sub_pages(
    wiki_id: str, parentPageId: Optional[str] = None
) -> Optional[response_result.WikiPageResult]:
    """특정 위키 페이지의 하위 페이지들을 조회합니다."""
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages"
    params = {
        "parentPageId": parentPageId,
    }
    response = dooray_request.dooray_get(end_point, params)
    if response is None:
        return None

    header = response["header"]
    result = {"result": response["result"]}
    return response_result.WikiPageResult(**result)


def get_wiki_page(
    wiki_id: str, pageId: str
) -> Optional[response_result.WikiPageResultItem]:
    """특정 위키 페이지를 조회합니다."""
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages/{pageId}"
    response = dooray_request.dooray_get(end_point)
    if response is None:
        return None

    header = response["header"]
    result = response["result"]
    return response_result.WikiPageResultItem(**result)
