import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from Rotas import app
from JogoLobby import Cria_jogo

@pytest.mark.asyncio
async def test_adiciona_player():
    Cria_jogo(1)

    async with AsyncClient(app=app, base_url="http://test") as ac:

        response = await ac.get("/1/add/1")
        assert response.status_code == 200
        assert response.json() == ['jogador adicionado com sucesso']

        response = await ac.get("/1/add/2")
        assert response.status_code == 200
        assert response.json() == ['jogador adicionado com sucesso']

        response = await ac.get("/1/add/3")
        assert response.status_code == 200
        assert response.json() == ['jogador adicionado com sucesso']

        response = await ac.get("/1/add/4")
        assert response.status_code == 200
        assert response.json() == ['jogador adicionado com sucesso']

@pytest.mark.asyncio
async def test_jogador_existente():
    async with AsyncClient(app=app, base_url="http://test") as ac:

        response = await ac.get("1/add/1")
        assert response.status_code == 400
        assert response.json()["detail"] == "Jogador já foi adicionado"

        response = await ac.get("1/add/2")
        assert response.status_code == 400
        assert response.json()["detail"] == "Jogador já foi adicionado"


@pytest.mark.asyncio
async def test_falha_adicionar_excesso():
    async with AsyncClient(app=app, base_url="http://test") as ac:

        response = await ac.get("/1/add/5")
        assert response.status_code == 400
        assert response.json()["detail"] == 'Não foi possível adicionar o jogador. Cores ou objetivos esgotados.'

@pytest.mark.asyncio
async def test_falha_jogo_desconhecido():
    async with AsyncClient(app=app, base_url="http://test") as ac:

        response = await ac.get("3/add/1")
        assert response.status_code == 404
        assert response.json()["detail"] == "Jogo não encontrado"

        response = await ac.get("100/add/1")
        assert response.status_code == 404
        assert response.json()["detail"] == "Jogo não encontrado"

