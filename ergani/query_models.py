from __future__ import annotations

from typing import Any, Callable, Dict, List, Protocol, TypeVar, runtime_checkable

QueryPayload = Dict[str, Any]
ParsedQueryType = TypeVar("ParsedQueryType")
QueryParser = Callable[[Any], ParsedQueryType]


@runtime_checkable
class QueryRequest(Protocol):
    def serialize(self) -> QueryPayload:
        ...


def parse_query_object(
    payload: Any, parser: QueryParser[ParsedQueryType]
) -> ParsedQueryType:
    if not isinstance(payload, dict):
        raise ValueError("Expected query service payload to be an object")

    return parser(payload)


def parse_query_list(
    payload: Any, parser: QueryParser[ParsedQueryType]
) -> List[ParsedQueryType]:
    if payload is None:
        return []

    if not isinstance(payload, list):
        raise ValueError("Expected query service payload to be a list")

    return [parser(item) for item in payload]