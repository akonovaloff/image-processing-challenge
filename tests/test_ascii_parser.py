import pytest
from interface_ascii_parser.interface_ascii_parser import parse_response


class TestInterfaceAsciiParser:
    @pytest.mark.parametrize("raw_resp, expected_resp", [
        ("A_10V", {'parameter': 'A', 'value': 10, 'unit': 'V'}),
        ("B_5V", {'parameter': 'B', 'value': 5, 'unit': 'V'}),
        ("C_15A", {'parameter': 'C', 'value': 15, 'unit': 'A'}),
        ("D_255Hz", {'parameter': 'D', 'value': 255, 'unit': 'Hz'}),
        ("INVALID_STRING", None)
    ])
    def test_parse_response(self, raw_resp, expected_resp):
        actual_resp = parse_response(raw_resp)
        assert actual_resp == expected_resp, f"Actual: {actual_resp}, Expected: {expected_resp}"
