from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Sequence, Type, TypeVar


class MainStatus(str, Enum):
    SUBMITTED = "1"
    WITHDRAWN = "2"


class AnswerStatus(str, Enum):
    PENDING = "0"
    SUBMITTED = "1"


class AnswerAccept(str, Enum):
    REJECTED = "0"
    ACCEPTED = "1"
    AUTO_ACCEPTED = "2"
    EXPIRED_REJECTED = "3"


EnumT = TypeVar("EnumT", bound=Enum)


def _pick_string_value(payload: Dict[str, Any], keys: Sequence[str]) -> Optional[str]:
    for key in keys:
        if key not in payload:
            continue

        value = payload[key]
        if value is None:
            continue

        return str(value)

    return None


def _parse_enum(enum_type: Type[EnumT], value: Optional[str]) -> Optional[EnumT]:
    if value is None:
        return None

    try:
        return enum_type(value)
    except ValueError:
        return None


@dataclass(frozen=True)
class EssentialTermsAcceptanceStatus:
    main_status_code: Optional[str]
    main_status: Optional[MainStatus]
    answer_status_code: Optional[str]
    answer_status: Optional[AnswerStatus]
    answer_accept_code: Optional[str]
    answer_accept: Optional[AnswerAccept]
    answer_protocol: Optional[str]
    answer_date: Optional[str]
    raw_payload: Dict[str, Any]

    @classmethod
    def from_payload(cls, payload: Any) -> "EssentialTermsAcceptanceStatus":
        return parse_essential_terms_acceptance_status(payload)


def parse_essential_terms_acceptance_status(
    payload: Any,
) -> EssentialTermsAcceptanceStatus:
    if not isinstance(payload, dict):
        raise ValueError("Expected EX_BASE_06 status payload to be an object")

    main_status_code = _pick_string_value(
        payload,
        ["MainStatus", "mainStatus", "main_status", "mainstatus"],
    )
    answer_status_code = _pick_string_value(
        payload,
        ["AnswerStatus", "answerStatus", "answer_status", "answerstatus"],
    )
    answer_accept_code = _pick_string_value(
        payload,
        ["AnswerAccept", "answerAccept", "answer_accept", "answeraccept"],
    )
    answer_protocol = _pick_string_value(
        payload,
        ["AnswerProtocol", "answerProtocol", "answer_protocol", "answerprotocol"],
    )
    answer_date = _pick_string_value(
        payload,
        ["AnswerDate", "answerDate", "answer_date", "answerdate"],
    )

    return EssentialTermsAcceptanceStatus(
        main_status_code=main_status_code,
        main_status=_parse_enum(MainStatus, main_status_code),
        answer_status_code=answer_status_code,
        answer_status=_parse_enum(AnswerStatus, answer_status_code),
        answer_accept_code=answer_accept_code,
        answer_accept=_parse_enum(AnswerAccept, answer_accept_code),
        answer_protocol=answer_protocol,
        answer_date=answer_date,
        raw_payload=dict(payload),
    )
