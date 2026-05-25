from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from ergani.client import ErganiClient
from ergani.models import BusinessBranch

SINGLE_BRANCH_PAYLOAD = {
    "Aa": "0",
    "Address": "ΠΛΑΤΕΙΑ ΑΓ. ΘΕΟΔΩΡΩΝ 6 10561 ΑΘΗΝΑ",
    "YpiresiaSepe": "11010",
    "YpiresiaOaed": "101201",
    "Kad": "6210",
    "Kallikratis": "91860101",
    "StatusDescription": "Έναρξη απασχόλησης",
}

BRANCH_PAYLOAD = {
    "EX_BASE_02": {
        "Pararthma": [
            {
                "Aa": "0",
                "Address": "ΑΓ. ΜΑΡΙΝΑΣ 19400 ΚΟΡΩΠΙ",
            },
            {
                "Aa": "1",
                "Address": "ΛΕΒΙΔΟΥ 14562 ΚΗΦΙΣΙΑ",
            },
        ]
    }
}

SINGLE_BRANCH_RAW_PAYLOAD = {
    "Aa": "0",
    "Address": "ΠΛΑΤΕΙΑ ΑΓ. ΘΕΟΔΩΡΩΝ 6 10561 ΑΘΗΝΑ",
    "YpiresiaSepe": "11010",
    "YpiresiaOaed": "101201",
    "Kad": "6210",
    "Kallikratis": "91860101",
    "StatusDescription": "Έναρξη απασχόλησης",
}

BRANCH_RAW_PAYLOADS = [
    {
        "Aa": "0",
        "Address": "ΑΓ. ΜΑΡΙΝΑΣ 19400 ΚΟΡΩΠΙ",
    },
    {
        "Aa": "1",
        "Address": "ΛΕΒΙΔΟΥ 14562 ΚΗΦΙΣΙΑ",
    },
]


class BusinessBranchTests(TestCase):
    def test_business_branch_parse_reads_single_branch_payload(self) -> None:
        self.assertEqual(
            BusinessBranch.parse(SINGLE_BRANCH_PAYLOAD),
            BusinessBranch(
                branch_number=0,
                address="ΠΛΑΤΕΙΑ ΑΓ. ΘΕΟΔΩΡΩΝ 6 10561 ΑΘΗΝΑ",
                sepe_service_code="11010",
                oaed_service_code="101201",
                business_branch_activity_code="6210",
                kallikratis_municipal_code="91860101",
                status_description="Έναρξη απασχόλησης",
                raw_payload=SINGLE_BRANCH_RAW_PAYLOAD,
            ),
        )

    def test_business_branch_parse_many_reads_wrapped_response(self) -> None:
        self.assertEqual(
            BusinessBranch.parse_many(BRANCH_PAYLOAD),
            [
                BusinessBranch(
                    branch_number=0,
                    address="ΑΓ. ΜΑΡΙΝΑΣ 19400 ΚΟΡΩΠΙ",
                    sepe_service_code=None,
                    oaed_service_code=None,
                    business_branch_activity_code=None,
                    kallikratis_municipal_code=None,
                    status_description=None,
                    raw_payload=BRANCH_RAW_PAYLOADS[0],
                ),
                BusinessBranch(
                    branch_number=1,
                    address="ΛΕΒΙΔΟΥ 14562 ΚΗΦΙΣΙΑ",
                    sepe_service_code=None,
                    oaed_service_code=None,
                    business_branch_activity_code=None,
                    kallikratis_municipal_code=None,
                    status_description=None,
                    raw_payload=BRANCH_RAW_PAYLOADS[1],
                ),
            ],
        )

    def test_business_branch_parse_requires_object_payload(self) -> None:
        with self.assertRaises(ValueError):
            BusinessBranch.parse("invalid")

    def test_business_branch_parse_many_accepts_single_branch_payload(self) -> None:
        self.assertEqual(
            BusinessBranch.parse_many({"EX_BASE_02": {"Pararthma": SINGLE_BRANCH_PAYLOAD}}),
            [
                BusinessBranch(
                    branch_number=0,
                    address="ΠΛΑΤΕΙΑ ΑΓ. ΘΕΟΔΩΡΩΝ 6 10561 ΑΘΗΝΑ",
                    sepe_service_code="11010",
                    oaed_service_code="101201",
                    business_branch_activity_code="6210",
                    kallikratis_municipal_code="91860101",
                    status_description="Έναρξη απασχόλησης",
                    raw_payload=SINGLE_BRANCH_RAW_PAYLOAD,
                )
            ],
        )

    def test_get_branch_details_uses_execute_service_and_parses_wrapped_response(self) -> None:
        client = ErganiClient("username", "password", "https://example.test")
        response = Mock(spec=Response)
        response.json.return_value = BRANCH_PAYLOAD

        with patch.object(
            client, "_execute_service", return_value=response
        ) as execute_service_mock:
            result = client.get_branch_details()

        self.assertEqual(
            result,
            [
                BusinessBranch(
                    branch_number=0,
                    address="ΑΓ. ΜΑΡΙΝΑΣ 19400 ΚΟΡΩΠΙ",
                    sepe_service_code=None,
                    oaed_service_code=None,
                    business_branch_activity_code=None,
                    kallikratis_municipal_code=None,
                    status_description=None,
                    raw_payload=BRANCH_RAW_PAYLOADS[0],
                ),
                BusinessBranch(
                    branch_number=1,
                    address="ΛΕΒΙΔΟΥ 14562 ΚΗΦΙΣΙΑ",
                    sepe_service_code=None,
                    oaed_service_code=None,
                    business_branch_activity_code=None,
                    kallikratis_municipal_code=None,
                    status_description=None,
                    raw_payload=BRANCH_RAW_PAYLOADS[1],
                ),
            ],
        )
        execute_service_mock.assert_called_once_with("EX_BASE_02")

    def test_get_branch_details_returns_empty_list_for_no_content(self) -> None:
        client = ErganiClient("username", "password", "https://example.test")

        with patch.object(
            client, "_execute_service", return_value=None
        ) as execute_service_mock:
            result = client.get_branch_details()

        self.assertEqual(result, [])
        execute_service_mock.assert_called_once_with("EX_BASE_02")
