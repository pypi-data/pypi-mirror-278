from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CaseSearchQueryParams:
    suites_query: str
    cases_query: str
    host: str
    user: str
    password: str
    dbname: str
    port: str


@dataclass
class Prefetch:
    group_key: str
    fk_key: str
    instances: list[dict[str, Any]]


@dataclass
class DataSetObject:
    parent_key: Optional[str]
    pk_key: str
    instances: list[dict[str, Any]]
