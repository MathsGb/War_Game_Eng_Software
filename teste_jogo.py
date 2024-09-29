import pytest
from JogoLobby import Jogo, calcula_exercitos_iniciais, JogadorFactoryConcreto

# Testando a criação de jogo e inicialização
def test_criacao_jogo():
    jogo = Jogo(id=1)
    assert jogo.id == 1
    assert jogo.lista_jogadores == {}
    assert jogo.ordem_jogadores == []

# Testando o cálculo de exércitos iniciais
@pytest.mark.parametrize("num_jogadores, expected_exercitos", [
    (2, 40),
    (3, 35),
    (4, 30),
    (5, 20)
])
def test_calcula_exercitos_iniciais(num_jogadores, expected_exercitos):
    assert calcula_exercitos_iniciais(num_jogadores) == expected_exercitos

# Testando a adição de jogadores usando o Factory Method
def test_adicionar_jogador():
    jogo = Jogo(id=1)
    factory = JogadorFactoryConcreto()
    
    # Adiciona jogador com factory
    novo_jogador = factory.criar_jogador(id_jogador=1, cor="vermelho", objetivo="Chegar a lua")
    assert novo_jogador.id == 1
    assert novo_jogador.cor_exercito == "vermelho"
    assert novo_jogador.objetivo == "Chegar a lua"
    
    jogo.add_jogador(1)
    assert len(jogo.lista_jogadores) == 1

# Testando a distribuição de territórios
def test_distribuir_territorios():
    jogo = Jogo(id=1)
    jogo.add_jogador(1)
    jogo.add_jogador(2)

    distribuicao = jogo.distribuir_territorios()
    assert len(distribuicao[1]) + len(distribuicao[2]) == len(Jogo.TERRITORIOS)

# Testando a distribuição de exércitos
def test_distribuir_exercitos():
    jogo = Jogo(id=1)
    jogo.add_jogador(1)
    jogo.add_jogador(2)

    exercitos_distribuidos = jogo.distribuir_exercitos()
    assert exercitos_distribuidos[1] == calcula_exercitos_iniciais(2)
    assert exercitos_distribuidos[2] == calcula_exercitos_iniciais(2)

# Testando a alocação de exércitos
def test_alocar_exercitos():
    jogo = Jogo(id=1)
    jogo.add_jogador(1)
    jogo.distribuir_exercitos()
    
    alocacao = jogo.alocar_exercitos(1, "Território 1", 5)
    assert jogo.lista_jogadores[1].exercitos == calcula_exercitos_iniciais(1) - 5
    assert alocacao["Território 1"] == 5

# Testando que o método de alocação não funciona com jogadores inexistentes
def test_alocar_exercitos_jogador_nao_existente():
    jogo = Jogo(id=1)
    resultado = jogo.alocar_exercitos(99, "Território 1", 5)
    assert resultado == "Jogador não encontrado"
