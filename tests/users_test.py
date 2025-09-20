from fastapi.testclient import TestClient
from buscabook.main import app

client = TestClient(app)

#Teste da rota de cadastro de usuários
def test_register():

    response = client.post(
        "/auth/register",
        json={
            "name": "example",
            "email": "example@gmail.com",
            "password": "1234"
        }
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Usuário cadastrado com sucesso! example@gmail.com"}

#teste da rota de login de usuários
def test_login():

    response = client.post(
        "/auth/login",
        json={
            "email": "example@gmail.com",
            "password": "1234"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

