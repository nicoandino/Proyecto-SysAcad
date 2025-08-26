import pytest
from app.mapping import UniversidadMapping
from test.instancias import nuevauniversidad

@pytest.mark.resourceuniversidad
def test_obtener_por_id(client):
    universidad = nuevauniversidad(nombre="Universidad Nacional de San Rafael", sigla="UNSR")
    client.application.db.session.add(universidad)
    client.application.db.session.commit()

    response = client.get(f'/api/v1/universidad/{universidad.id}')
    assert response.status_code == 200

    data = response.get_json()
    universidad_obtenida = UniversidadMapping().load(data)
    assert universidad_obtenida.id == universidad.id
    assert universidad_obtenida.nombre == "Universidad Nacional de San Rafael"
    assert universidad_obtenida.sigla == "UNSR"

@pytest.mark.resourceuniversidad
def test_obtener_todos(client):
    utn = nuevauniversidad(nombre="UTN San Rafael", sigla="UTNSR")
    uncuyo = nuevauniversidad(nombre="UNCuyo", sigla="UNC")
    client.application.db.session.add_all([utn, uncuyo])
    client.application.db.session.commit()

    response = client.get('/api/v1/universidad')
    assert response.status_code == 200

    data = response.get_json()
    universidades = UniversidadMapping().load(data, many=True)
    nombres = [u.nombre for u in universidades]
    assert "UTN San Rafael" in nombres
    assert "UNCuyo" in nombres
    assert len(universidades) == 2
