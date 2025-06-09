import pytest
from scoring import calculate_score, recommend_next_level

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

def test_recommend_none_when_level7():
    data = {f: 1 for f in ALL_FACTORS}
    assert recommend_next_level(data) is None

def test_recommend_network_for_zero_input():
    data = {f: 0 for f in ALL_FACTORS}
    rec = recommend_next_level(data)
    assert rec["factor"] == "network_protection"
    assert rec["delta_score"] == 18

def test_recommend_email_to_reach_level_from_score87():
    data = {f: 1 for f in ALL_FACTORS}
    data["email_practices"] = 0
    # current_score = 98 - 13 = 85, level=6, next_threshold=90, needs +5
    rec = recommend_next_level(data)
    assert rec["factor"] == "email_practices"
    assert rec["delta_score"] == 13
