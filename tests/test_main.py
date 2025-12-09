from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_get_years():
    response = client.get("/years/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "1939" in response.json()  

def test_get_year_details():
    response = client.get("/year/1939")
    assert response.status_code == 200
    data = response.json()
    assert data