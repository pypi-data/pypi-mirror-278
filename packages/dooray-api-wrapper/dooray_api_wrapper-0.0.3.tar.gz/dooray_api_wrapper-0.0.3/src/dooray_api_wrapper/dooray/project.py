from typing import Dict, List, Union, Optional

from dooray_api_wrapper.common import dooray_request
from dooray_api_wrapper.const.const import Scope, Type, State
from dooray_api_wrapper.structure import response_result, response_header


def get_project_list(
    page: int = 0,
    size: int = 0,
    scope: Scope = Scope.PUBLIC,
    type: Type = Type.PUBLIC,
    state: State = State.ACTIVE,
):
    end_point = f"/project/v1/projects"
    params = {
        "page": page,
        "size": size,
        "scope": scope.value,
        "type": type.value,
        "state": state.value,
    }
    return dooray_request.dooray_get(end_point, params)


def get_project(project_id: str):
    end_point = f"/project/v1/projects/{project_id}"
    return dooray_request.dooray_get(end_point)


def response(
    data: Dict,
) -> Optional[
    List[Union[response_header.ResponseHeader, response_result.ProjectResult]]
]:
    header = data["header"]
    result = {"result": data["result"]}
    return [
        response_header.ResponseHeader(**header),
        response_result.ProjectResult(**result),
    ]
