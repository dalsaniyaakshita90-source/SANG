from backend.agriculture_query import query_agriculture


def test_pest_query():
    result = query_agriculture(
        "My crop has a pest problem in Rajkot"
    )

    assert result["understood"]["location"] == "Rajkot"
    assert result["understood"]["problem"] == "Crop Pest Infestation"

    assert len(result["results"]) == 1
    assert result["results"][0]["problem"]["id"] == "AP001"

    assert result["results"][0]["helpers"][0]["id"] == "H001"
    assert result["results"][0]["resources"][0]["id"] == "AR001"


def test_irrigation_query():
    result = query_agriculture(
        "I have an irrigation problem in Ahmedabad"
    )

    assert result["understood"]["location"] == "Ahmedabad"
    assert result["understood"]["problem"] == "Irrigation Challenge"

    assert len(result["results"]) == 1
    assert result["results"][0]["problem"]["id"] == "AP002"

    assert result["results"][0]["helpers"][0]["id"] == "H002"
    assert result["results"][0]["resources"][0]["id"] == "AR002"


def test_soil_query():
    result = query_agriculture(
        "My soil health is getting worse in Surat"
    )

    assert result["understood"]["location"] == "Surat"
    assert result["understood"]["problem"] == "Soil Health Problem"

    assert len(result["results"]) == 1
    assert result["results"][0]["problem"]["id"] == "AP003"

    assert result["results"][0]["helpers"][0]["id"] == "H003"
    assert result["results"][0]["resources"][0]["id"] == "AR003"


def test_unknown_problem_is_rejected():
    result = query_agriculture(
        "I need help with quantum physics in Rajkot"
    )

    assert result["understood"]["location"] == "Rajkot"
    assert result["understood"]["problem"] is None
    assert result["results"] == []


def test_unknown_location():
    result = query_agriculture(
        "My crop has a pest problem in Mumbai"
    )

    assert result["understood"]["location"] == "Mumbai"
    assert result["understood"]["location_mentioned"] is True
    assert result["understood"]["problem"] == "Crop Pest Infestation"

    assert result["results"] == []