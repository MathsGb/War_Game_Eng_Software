from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from JogoLobby import Jogo

app = FastAPI()
lista_jogos = {}

@app.get("/")
def home():
    return {"Olá": "Vamos começar!",
            "Atualmente há:": f"{len(lista_jogos)} jogos"}

@app.get("/create/{id_novo_jogo}")
def novo_jogo(id_novo_jogo: int):
    lista_jogos[id_novo_jogo] = Jogo(id_novo_jogo)
    return RedirectResponse(url="/")

@app.get("/{id_jogo}")
def jogo_lobby(id_jogo: int):
    try:
        jogo_atual = lista_jogos[id_jogo]
        return {1: f'Você agora está dentro de um jogo de número {jogo_atual.id}',
                2: f'Atualmente tenho {len(jogo_atual.lista_jogadores)} jogadores presentes',
                3: f'Os jogadores atualmente são: {jogo_atual.exibir_jogadores()}'}
    except KeyError:
        return RedirectResponse(url="/")

@app.get("/{id_jogo}/add/{player_id}")
def adiciona_player(id_jogo: int, player_id: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    if player_id in jogo_atual.lista_jogadores:
        return {"erro": "Jogador já adicionado"}
    jogo_atual.add_jogador(player_id)
    return {'jogador adicionado com sucesso'}

@app.get("/{id_jogo}/definir_ordem")
def definir_ordem(id_jogo: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    ordem = jogo_atual.definir_ordem_jogadores()
    return {"Ordem dos jogadores": ordem}

@app.get("/{id_jogo}/ordem")
def obter_ordem(id_jogo: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    ordem = jogo_atual.get_ordem_jogadores()
    return {"Ordem dos jogadores": ordem}

@app.get("/{id_jogo}/distribuir_territorios")
def distribuir_territorios(id_jogo: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    distribuicao = jogo_atual.distribuir_territorios()
    return {"Distribuição dos territórios": distribuicao}

@app.get("/{id_jogo}/territorios")
def obter_territorios(id_jogo: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    territorios = jogo_atual.exibir_territorios()
    return {"Territórios distribuídos": territorios}

@app.get("/{id_jogo}/distribuir_exercitos")
def distribuir_exercitos(id_jogo: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    distribuicao = jogo_atual.distribuir_exercitos()
    return {"Distribuição dos exércitos": distribuicao}

@app.get("/{id_jogo}/exercitos")
def obter_exercitos(id_jogo: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    exercitos = jogo_atual.exibir_exercitos()
    return {"Exércitos distribuídos": exercitos}

@app.get("/{id_jogo}/alocar_exercitos/{player_id}/{territorio}/{quantidade}")
def alocar_exercitos(id_jogo: int, player_id: int, territorio: str, quantidade: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    resultado = jogo_atual.alocar_exercitos(player_id, territorio, quantidade)
    return {"Resultado da alocação": resultado}

@app.get("/{id_jogo}/alocacao_exercitos")
def obter_alocacao_exercitos(id_jogo: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    alocacao = jogo_atual.exibir_alocacao_exercitos()
    return {"Alocação dos exércitos": alocacao}

@app.get("/{id_jogo}/exercitos_por_territorio")
def obter_exercitos_por_territorio(id_jogo: int):
    if id_jogo not in lista_jogos:
        return {"erro": "Jogo não encontrado"}
    jogo_atual = lista_jogos[id_jogo]
    exercitos_por_territorio = jogo_atual.exibir_exercitos_por_territorio()
    return {"Exércitos por Território": exercitos_por_territorio}
