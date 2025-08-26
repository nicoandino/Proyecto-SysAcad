import pytest
from app.services import TipoDocumentoService
from test.instancias import nuevotipodocumento

@pytest.mark.servicetipodocumento
def test_crear_tipodocumento(client):
    doc = nuevotipodocumento()
    client.application.db.session.add(doc)
    client.application.db.session.commit()

    assert doc is not None
    assert doc.id is not None
    assert doc.dni == 46291002
    assert doc.libreta_civica == "nacional"
    assert doc.libreta_enrolamiento == "militar"
    assert doc.pasaporte == "AR123456"

@pytest.mark.servicetipodocumento
def test_buscar_por_id(client):
    doc = nuevotipodocumento()
    client.application.db.session.add(doc)
    client.application.db.session.commit()

    resultado = TipoDocumentoService.buscar_por_id(doc.id)
    assert resultado is not None
    assert resultado.dni == 46291002
    assert resultado.libreta_civica == "nacional"

@pytest.mark.servicetipodocumento
def test_buscar_todos(client):
    doc1 = nuevotipodocumento()
    doc2 = nuevotipodocumento(48291002, "cívica", "enrolamiento", "CD987654")
    client.application.db.session.add_all([doc1, doc2])
    client.application.db.session.commit()

    documentos = TipoDocumentoService.buscar_todos()
    assert documentos is not None
    assert len(documentos) == 2

@pytest.mark.servicetipodocumento
def test_actualizar_tipodocumento(client):
    doc = nuevotipodocumento()
    client.application.db.session.add(doc)
    client.application.db.session.commit()

    doc.dni = 89291002
    doc.libreta_civica = "actualizada"
    actualizado = TipoDocumentoService.actualizar(doc.id, doc)

    assert actualizado.dni == 89291002
    assert actualizado.libreta_civica == "actualizada"

@pytest.mark.servicetipodocumento
def test_borrar_tipodocumento(client):
    doc = nuevotipodocumento()
    client.application.db.session.add(doc)
    client.application.db.session.commit()

    borrado = TipoDocumentoService.borrar_por_id(doc.id)
    assert borrado is True

    resultado = TipoDocumentoService.buscar_por_id(doc.id)
    assert resultado is None
