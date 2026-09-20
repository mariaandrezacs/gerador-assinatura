import io

import pytest
from PIL import Image

from app import app, SIGNATURE_WIDTH, SIGNATURE_HEIGHT

FORM_DATA = {
    "name": "Maria Teste",
    "title": "Analista",
    "department": "TI",
    "phone": "(82) 99999-0000",
    "email": "maria@teste.com",
    "website": "teste.com.br",
}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_form_page(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_generate_signature(client):
    resp = client.post("/generate_signature", data=FORM_DATA)
    assert resp.status_code == 200

    with Image.open("static/assinatura_email.png") as img:
        assert img.size == (SIGNATURE_WIDTH, SIGNATURE_HEIGHT)


def test_generate_signature_with_background(client):
    data = dict(FORM_DATA)
    data["background"] = (io.BytesIO(b"fake"), "fundo.png")  # extensão válida, conteúdo inválido
    resp = client.post("/generate_signature", data=data, content_type="multipart/form-data")
    # imagem inválida não deve quebrar a geração — usa o fundo padrão
    assert resp.status_code == 200
    assert "não é uma imagem válida" in resp.get_data(as_text=True)
