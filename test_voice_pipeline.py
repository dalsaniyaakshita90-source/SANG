from backend.voice_pipeline import build_voice_pipeline


def get_route(result):
    classify_stage = next(
        stage for stage in result["pipeline"]
        if stage["stage"] == "CLASSIFY"
    )
    return classify_stage["route"]


def test_voice_information():
    result = build_voice_pipeline(
        "What is crop pest management?",
        "INFORMATION",
        {},
    )

    assert get_route(result) == "INFORMATION"


def test_voice_assistance():
    result = build_voice_pipeline(
        "I have a pest problem in Rajkot",
        "ASSISTANCE",
        {},
    )

    assert get_route(result) == "ASSISTANCE"


def test_voice_emergency():
    result = build_voice_pipeline(
        "There is a fire emergency",
        "EMERGENCY",
        {},
    )

    assert get_route(result) == "EMERGENCY"


def test_voice_hindi_assistance():
    result = build_voice_pipeline(
        "Meri fasal mein keede lag gaye hain Rajkot mein",
        "ASSISTANCE",
        {},
    )

    assert get_route(result) == "ASSISTANCE"


def test_voice_gujarati_assistance():
    result = build_voice_pipeline(
        "Mane Ahmedabad ma pani ni samasya chhe",
        "ASSISTANCE",
        {},
    )

    assert get_route(result) == "ASSISTANCE"