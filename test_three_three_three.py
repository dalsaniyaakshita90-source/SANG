from backend.three_three_three import (
    classify_333_intent,
    start_333_session,
    continue_333_session,
)


def test_333_assistance_route():
    result = start_333_session(
        "I need help with irrigation in Ahmedabad"
    )

    assert result["route"] == "ASSISTANCE"
    assert result["status"] == "ROUTED"
    assert result["result"]["results"][0]["problem"]["id"] == "AP002"


def test_333_emergency_route():
    result = start_333_session(
        "This is an emergency, help now"
    )

    assert result["route"] == "EMERGENCY"
    assert result["status"] == "ESCALATE"
    assert result["result"] is None


def test_333_missing_location():
    result = start_333_session(
        "I need help with irrigation"
    )

    assert result["route"] == "ASSISTANCE"
    assert result["status"] == "NEEDS_INFORMATION"
    assert result["missing_information"] == ["location"]
    assert result["prompt"] is not None


def test_333_multi_turn_completion():
    first = start_333_session(
        "I need help with irrigation"
    )

    second = continue_333_session(
        first,
        "Ahmedabad"
    )

    assert second["status"] == "ROUTED"
    assert second["missing_information"] == []
    assert second["result"]["results"][0]["problem"]["id"] == "AP002"


def test_333_unknown_request():
    result = start_333_session(
        "Tell me something random"
    )

    assert result["route"] == "UNKNOWN"
    assert result["status"] == "ESCALATE"
    assert result["result"] is None