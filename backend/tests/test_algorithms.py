from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_sort_bubble():
    response = client.post("/api/sort", json={"values":[4, 1, 3, 2], "algorithm":"bubble"})
    assert response.status_code == 200
    assert response.json()["result"] == [1, 2, 3, 4]
    assert len(response.json()["steps"]) > 1

def test_sort_algorithms():
    for algorithm in ["selection", "insertion", "merge", "quick"]:
        response = client.post("/api/sort", json={"values":[8, 2, 5, 2, 1], "algorithm":algorithm})
        assert response.status_code == 200
        assert response.json()["result"] == [1, 2, 2, 5, 8]

def test_binary_search_found_and_missing():
    found = client.post("/api/binary-search", json={"values":[9, 1, 4, 7], "target":4}).json()
    missing = client.post("/api/binary-search", json={"values":[1, 4, 7], "target":3}).json()
    assert found["found"] is True
    assert found["sorted_values"][found["index"]] == 4
    assert missing["found"] is False

def test_remove_duplicates_sorted_input():
    response = client.post("/api/remove-duplicates", json={"values":[1, 1, 2, 3, 3]})
    assert response.json()["result"] == [1, 2, 3]
