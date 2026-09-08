from backend.query_engine import query_sang


def test_python():
    result = query_sang("Python")
    assert len(result["results"]) == 1
    assert result["results"][0]["person"] == "Rahul"
    assert result["results"][0]["match"]["target_id"] == "PR002"


def test_python_case_insensitive():
    result = query_sang("PYTHON")
    assert len(result["results"]) == 1
    assert result["results"][0]["person"] == "Rahul"


def test_location():
    result = query_sang("Ahmedabad")
    assert len(result["results"]) == 1
    assert result["results"][0]["person"] == "Rahul"


def test_combined_query():
    result = query_sang("Python in Ahmedabad")
    assert len(result["results"]) == 1
    assert result["results"][0]["person"] == "Rahul"


def test_agriculture():
    result = query_sang("agriculture")
    assert len(result["results"]) == 1
    assert result["results"][0]["person"] == "Rahul"


def test_sustainability():
    result = query_sang("sustainability")
    assert len(result["results"]) == 2
    assert all(item["person"] == "Priya" for item in result["results"])


def test_teaching():
    result = query_sang("teaching")
    assert result["results"] == []


def test_conflicting_location():
    result = query_sang("python in Surat")
    assert result["results"] == []


def test_conflicting_category_location():
    result = query_sang("agriculture in Surat")
    assert result["results"] == []


def test_unknown_query():
    result = query_sang("quantum physics")
    assert result["results"] == []


def test_empty_query():
    result = query_sang("")
    assert result["results"] == []