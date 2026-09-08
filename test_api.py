from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_people():
    response = client.get("/people")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_problems():
    response = client.get("/problems")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_opportunities():
    response = client.get("/opportunities")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_resources():
    response = client.get("/resources")
    assert response.status_code == 200


def test_python_query():
    response = client.get("/query", params={"query": "Python"})

    assert response.status_code == 200

    data = response.json()

    assert data["results"][0]["person"] == "Rahul"
    assert data["results"][0]["match"]["target_id"] == "PR002"


def test_unknown_query():
    response = client.get("/query", params={"query": "quantum physics"})

    assert response.status_code == 200
    assert response.json()["results"] == []


def test_conflicting_query():
    response = client.get("/query", params={"query": "python in Surat"})

    assert response.status_code == 200
    assert response.json()["results"] == []