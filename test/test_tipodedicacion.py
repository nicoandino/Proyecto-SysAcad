import pytest
from app.mapping import TipoDedicacionMapping
from test.instancias import nuevotipodedicacion

@pytest.mark.resourcetipodedicacion
def test_obtener_por_id(client):
    tipo = nuevotipodedicacion(nombre="Exclusiva", observacion="Dedicación completa al cargo")
    client.application.db.session.add(tipo)
    client.application.db.session.commit()

    response = client.get(f'/api/v1/tipodedicacion/{tipo.id}')
    assert response.status_code == 200

    data = response.get_json()
    tipo_obtenido = TipoDedicacionMapping().load(data)
    assert tipo_obtenido.id == tipo.id
    assert tipo_obtenido.nombre == "Exclusiva"
    assert tipo_obtenido.observacion == "Dedicación completa al cargo"

@pytest.mark.resourcetipodedicacion
def test_obtener_todos(client):
    tipo1 = nuevotipodedicacion(nombre="Simple", observacion="Dedicación mínima")
    tipo2 = nuevotipodedicacion(nombre="Parcial", observacion="Dedicación intermedia")
    client.application.db.session.add_all([tipo1, tipo2])
    client.application.db.session.commit()

    response = client.get('/api/v1/tipodedicacion')
    assert response.status_code == 200

    data = response.get_json()
    tipos = TipoDedicacionMapping().load(data, many=True)
    nombres = [t.nombre for t in tipos]
    observaciones = [t.observacion for t in tipos]

    assert "Simple" in nombres
    assert "Parcial" in nombres
    assert "Dedicación mínima" in observaciones
    assert "Dedicación intermedia" in observaciones
    assert len(tipos) == 2
