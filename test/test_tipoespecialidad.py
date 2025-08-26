import pytest
from app.mapping import TipoEspecialidadMapping
from test.instancias import nuevotipoespecialidad

@pytest.mark.resourceespecialidad
def test_obtener_por_id(client):
    tipo = nuevotipoespecialidad(nombre="Cardiología")
    client.application.db.session.add(tipo)
    client.application.db.session.commit()

    response = client.get(f'/api/v1/tipoespecialidad/{tipo.id}')
    assert response.status_code == 200

    data = response.get_json()
    tipo_obtenido = TipoEspecialidadMapping().load(data)
    assert tipo_obtenido.id == tipo.id
    assert tipo_obtenido.nombre == "Cardiología"

@pytest.mark.resourceespecialidad
def test_obtener_todos(client):
    tipo1 = nuevotipoespecialidad(nombre="Cardiología")
    tipo2 = nuevotipoespecialidad(nombre="Pediatría")
    client.application.db.session.add_all([tipo1, tipo2])
    client.application.db.session.commit()

    response = client.get('/api/v1/tipoespecialidad')
    assert response.status_code == 200

    data = response.get_json()
    tipos = TipoEspecialidadMapping().load(data, many=True)
    nombres = [t.nombre for t in tipos]

    assert "Cardiología" in nombres
    assert "Pediatría" in nombres
    assert len(tipos) == 2
