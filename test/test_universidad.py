import pytest
from app.mapping import UniversidadMapping
from test.instancias import nuevauniversidad

@pytest.mark.resourceuniversidad
def test_obtener_por_id(client):
    uni = nuevauniversidad(nombre="Universidad Nacional", sigla="UN")
    client.application.db.session.add(uni)
    client.application.db.session.commit()

    response = client.get(f'/api/v1/universidad/{uni.id}')
    assert response.status_code == 200

    data = response.get_json()
    universidad_obtenida = UniversidadMapping().load(data)
    assert universidad_obtenida.id == uni.id
    assert universidad_obtenida.nombre == "Universidad Nacional"
    assert universidad_obtenida.sigla == "UN"

@pytest.mark.resourceuniversidad
def test_obtener_todos(client):
    uni1 = nuevauniversidad(nombre="Universidad Nacional", sigla="UN")
    uni2 = nuevauniversidad(nombre="Universidad Tecnológica", sigla="UTN")
    client.application.db.session.add_all([uni1, uni2])
    client.application.db.session.commit()

    response = client.get('/api/v1/universidad')
    assert response.status_code == 200

    data = response.get_json()
    universidades = UniversidadMapping().load(data, many=True)
    nombres = [u.nombre for u in universidades]

    assert "Universidad Nacional" in nombres
    assert "Universidad Tecnológica" in nombres
    assert len(universidades) == 2
