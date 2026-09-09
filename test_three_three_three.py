from backend.three_three_three import start_333_session


def test_333_information_route():
    result = start_333_session(
        "What is a crop pest?"
    )

    assert result["route"] == "INFORMATION"
    assert result["status"] == "ROUTED"


def test_333_assistance_route():
    result = start_333_session(
        "I need help with my crop pest problem in Rajkot"
    )

    assert result["route"] == "ASSISTANCE"
    assert result["status"] == "ROUTED"


def test_333_emergency_route():
    result = start_333_session(
        "This is an emergency, help now"
    )

    assert result["route"] == "EMERGENCY"
    assert result["status"] == "ESCALATE"
    assert result["result"]["detected"] is True
    assert result["result"]["emergency_type"] == "general"
    assert result["result"]["contact"] == "112"


def test_333_unknown_route():
    result = start_333_session(
        "xyz random request"
    )

    assert result["route"] == "UNKNOWN"
    assert result["status"] == "ESCALATE"

def test_india_emergency_ruleset():
    from backend.emergency_layer import identify_emergency

    result = identify_emergency(
        "There is a fire emergency",
        country_code="IN",
    )

    assert result["country"] == "India"
    assert result["country_code"] == "IN"
    assert result["emergency_type"] == "fire"
    assert result["contact"] == "101"
    assert result["escalation"] == "IMMEDIATE"


def test_india_medical_emergency_ruleset():
    from backend.emergency_layer import identify_emergency

    result = identify_emergency(
        "Someone is unconscious and needs an ambulance",
        country_code="IN",
    )

    assert result["country"] == "India"
    assert result["country_code"] == "IN"
    assert result["emergency_type"] == "medical"
    assert result["contact"] == "108"
    assert result["escalation"] == "IMMEDIATE"


def test_unknown_country_falls_back_safely():
    from backend.emergency_layer import identify_emergency

    result = identify_emergency(
        "There is an emergency",
        country_code="XX",
    )

    assert result["country"] == "India"
    assert result["country_code"] == "XX"
    assert result["contact"] == "112"
    assert result["escalation"] == "IMMEDIATE"