from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Sequence

ParameterCatalogType = Literal[
    "Sepe",
    "KallikratisDhmos",
    "WorkCardDelayReason",
]


@dataclass(frozen=True)
class ParameterOption:
    code: Optional[str]
    value: Optional[str]
    description: Optional[str]
    extra: Optional[str] = None


def _pick_string_value(payload: Dict[str, Any], keys: Sequence[str]) -> Optional[str]:
    for key in keys:
        if key not in payload:
            continue

        value = payload[key]
        if value is None:
            continue

        return str(value)

    return None


def parse_parameter_option(payload: Any) -> ParameterOption:
    if not isinstance(payload, dict):
        raise ValueError("Expected parameter option to be an object")

    code = _pick_string_value(
        payload,
        ["code", "Code", "id", "Id", "ID", "key", "Key"],
    )
    value = _pick_string_value(
        payload,
        ["value", "Value", "name", "Name", "title", "Title"],
    )
    description = _pick_string_value(
        payload,
        [
            "description",
            "Description",
            "desc",
            "Desc",
            "label",
            "Label",
            "text",
            "Text",
        ],
    )
    extra = _pick_string_value(payload, ["extra", "Extra"])

    if value is None:
        value = description

    return ParameterOption(
        code=code,
        value=value,
        description=description,
        extra=extra,
    )


def parse_parameter_options(data: Any) -> List[ParameterOption]:
    if data is None:
        return []

    if isinstance(data, dict):
        if "EX_BASE_03" in data:
            data = data["EX_BASE_03"]

        if isinstance(data, dict) and "Param" in data:
            data = data["Param"]

    if not isinstance(data, list):
        raise ValueError("Expected parameter options response to be a list")

    return [parse_parameter_option(item) for item in data]
