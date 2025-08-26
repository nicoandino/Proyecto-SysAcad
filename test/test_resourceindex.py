import pytest

@pytest.mark.resourceindex
def test_index(client):
    response = client.get('/api/v1/')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert isinstance(data, dict)
    assert "mensaje" in data
    assert data["mensaje"] == "API funcionando"
