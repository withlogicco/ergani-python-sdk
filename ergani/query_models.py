from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

MIN_MONTHLY_STATUS_REPORT_YEAR = 2000
MAX_MONTHLY_STATUS_REPORT_YEAR = 2100


@dataclass(frozen=True)
class MonthlyStatusRequest:
    report_year: int
    report_month: int

    def __post_init__(self) -> None:
        if (
            not MIN_MONTHLY_STATUS_REPORT_YEAR
            <= self.report_year
            <= MAX_MONTHLY_STATUS_REPORT_YEAR
        ):
            raise ValueError(
                "report_year must be between "
                f"{MIN_MONTHLY_STATUS_REPORT_YEAR} and {MAX_MONTHLY_STATUS_REPORT_YEAR}"
            )

        if not 1 <= self.report_month <= 12:
            raise ValueError("report_month must be between 1 and 12")

    def serialize(self) -> Dict[str, Any]:
        return {
            "ReportYear": self.report_year,
            "ReportMonth": self.report_month,
        }


@dataclass(frozen=True)
class MonthlyStatusRecord:
    raw_payload: Dict[str, Any]


def parse_monthly_status_record(payload: Any) -> MonthlyStatusRecord:
    if not isinstance(payload, dict):
        raise ValueError("Expected monthly status record to be an object")

    return MonthlyStatusRecord(raw_payload=dict(payload))


def parse_monthly_status_list(payload: Any) -> List[MonthlyStatusRecord]:
    if payload is None:
        return []

    if not isinstance(payload, list):
        raise ValueError("Expected monthly status response to be a list")

    return [parse_monthly_status_record(item) for item in payload]
