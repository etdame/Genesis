import pytest
from scoring import calculate_score

ALL_FACTORS = [
    "network_protection",
    "email_practices",
    "password_hygiene",
    "browser_metadata_hygiene",
    "open_source_usage",
    "self_hosted_vpn",
    "os_telemetry",
    "two_factor_authentication",
    "encryption_at_rest"
]

def test_all_ones_yields_98_and_no_tip():
    data = {f: 1 for f in ALL_FACTORS}
    result = calculate_score(data)
    assert result["score"] == 98
    assert result["level"] == 7
    assert result["next_tip"] is None

def test_all_zeros_yields_zero_score_and_network_tip():
    data = {f: 0 for f in ALL_FACTORS}
    result = calculate_score(data)
    assert result["score"] == 0
    assert result["level"] == 1
    assert result["next_tip"]["factor"] == "network_protection"

def test_self_hosted_vpn_ignored_when_no_vpn():
    data = {f: 0 for f in ALL_FACTORS}
    data["self_hosted_vpn"] = 1
    result = calculate_score(data)
    assert result["breakdown"]["self_hosted_vpn"] == 0
