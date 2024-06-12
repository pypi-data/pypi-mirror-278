import re
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
from enum import Enum

from src.const.const import Scope, Type, State


class SearchType(Enum):
    SEARCH = "search"
    MATCH = "match"
    FULLMATCH = "fullMatch"


class ProjectResultItem(BaseModel):
    id: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    state: Optional[State] = None
    scope: Optional[Scope] = None
    type: Optional[Type] = None
    organization: Optional[Dict] = None
    organizationId: Optional[str] = None
    drive: Optional[Dict] = None
    wiki: Optional[Dict] = None


class ProjectResult(BaseModel):
    result: List[ProjectResultItem]

    def find_project_by_title(
        self, title: str, search_type: SearchType = SearchType.SEARCH
    ) -> Optional[ProjectResultItem]:
        """프로젝트 목록에서 title에 해당하는 프로젝트를 찾아서 반환합니다.
        SEARCH: title에 해당하는 프로젝트를 찾아서 반환합니다.
        MATCH: title로 시작하는 프로젝트를 찾아서 반환합니다.
        FULLMATCH: title과 정확히 일치하는 프로젝트를 찾아서 반환합니다.
        """
        regex = re.compile(title)
        for project in self.result:
            if getattr(regex, search_type.value)(title) is not None:
                return project
        return None


class WikiResultItem(BaseModel):
    id: Optional[str] = None
    project: Optional[Dict] = None
    name: Optional[str] = None
    type: Optional[Type] = None
    scope: Optional[Scope] = None
    home: Optional[Dict] = None


class WikiResult(BaseModel):
    result: List[WikiResultItem]


class WikiPageResultItem(BaseModel):
    id: Optional[str] = None
    wikiId: Optional[str] = None
    version: Optional[str] = None
    parentPageId: Optional[str] = None
    subject: Optional[str] = None
    root: Optional[bool] = None
    creator: Optional[Dict] = None
    createdAt: Optional[str] = None
    body: Optional[Dict] = None
    referrers: Optional[List[Dict]] = None
    files: Optional[List[Dict]] = None


class WikiPageResult(BaseModel):
    result: List[WikiResultItem]
