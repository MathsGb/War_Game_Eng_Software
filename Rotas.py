from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from JogoLobby import Cria_jogo, lista_jogos

app = FastAPI()

def obter_jogo(id_jogo: int):
    """Função auxiliar para obter um jogo."""
    jogo = lista_jogos.get(id_jogo)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo

def obter_jogador(jogo, player_id: int):
    """Função auxiliar para obter um jogador em um jogo."""
    jogador = jogo.lista_jogadores.get(player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return jogador

@app.get("/")
def home():
    return {
        "mensagem": "Vamos começar!",
        "jogos_ativos": len(lista_jogos)
    }

@app.get("/create/{id_novo_jogo}")
def novo_jogo(id_novo_jogo: int):
    Cria_jogo(id_novo_jogo)
    return RedirectResponse(url="/")

@app.get("/{id_jogo}")
def jogo_lobby(id_jogo: int):
    jogo_atual = obter_jogo(id_jogo)
    return {
        "id": jogo_atual.id,
        "jogadores_presentes": len(jogo_atual.lista_jogadores),
        "jogadores": jogo_atual.exibir_jogadores()
    }

@app.get("/{id_jogo}/add/{player_id}")
def adiciona_player(id_jogo: int, player_id: int):
    jogo_atual = obter_jogo(id_jogo)
    if player_id in jogo_atual.lista_jogadores:
        raise HTTPException(status_code=400, detail="Jogador já adicionado")
    jogo_atual.add_jogador(player_id)
    return {"mensagem": "Jogador adicionado com sucesso"}

@app.get("/{id_jogo}/definir_ordem")
def definir_ordem(id_jogo: int):
    jogo_atual = obter_jogo(id_jogo)
    ordem = jogo_atual.definir_ordem_jogadores()
    return {"ordem_dos_jogadores": ordem}

@app.get("/{id_jogo}/ordem")
def obter_ordem(id_jogo: int):
    jogo_atual = obter_jogo(id_jogo)
    ordem = jogo_atual.get_ordem_jogadores()
    return {"ordem_dos_jogadores": ordem}

@app.get("/{id_jogo}/distribuir_territorios")
def distribuir_territorios(id_jogo: int):
    jogo_atual = obter_jogo(id_jogo)
    distribuicao = jogo_atual.distribuir_territorios()
    return {"distribuicao_dos_territorios": distribuicao}

@app.get("/{id_jogo}/territorios")
def obter_territorios(id_jogo: int):
    jogo_atual = obter_jogo(id_jogo)
    territorios = jogo_atual.exibir_territorios()
    return {"territorios_distribuidos": territorios}

@app.get("/{id_jogo}/distribuir_exercitos")
def distribuir_exercitos(id_jogo: int):
    jogo_atual = obter_jogo(id_jogo)
    distribuicao = jogo_atual.distribuir_exercitos()
    return {"distribuicao_dos_exercitos": distribuicao}

@app.get("/{id_jogo}/exercitos")
def obter_exercitos(id_jogo: int):
    jogo_atual = obter_jogo(id_jogo)
    exercitos = jogo_atual.exibir_exercitos()
    return {"exercitos_distribuidos": exercitos}

@app.get("/{id_jogo}/alocar_exercitos/{player_id}/{territorio}/{quantidade}")
def alocar_exercitos(id_jogo: int, player_id: int, territorio: str, quantidade: int):
    jogo_atual = obter_jogo(id_jogo)
    jogador = obter_jogador(jogo_atual, player_id)
    resultado = jogo_atual.alocar_exercitos(player_id, territorio, quantidade)
    return {"resultado_da_alocacao": resultado}

@app.get("/{id_jogo}/alocacao_exercitos")
def obter_alocacao_exercitos(id_jogo: int):
    jogo_atual = obter_jogo(id_jogo)
    alocacao = jogo_atual.exibir_alocacao_exercitos()
    return {"alocacao_dos_exercitos": alocacao}

@app.get("/{id_jogo}/exercitos_por_territorio")
def obter_exercitos_por_territorio(id_jogo: int):
    jogo_atual = obter_jogo(id_jogo)
    exercitos_por_territorio = jogo_atual.exibir_exercitos_por_territorio()
    return {"exercitos_por_territorio": exercitos_por_territorio}

@app.get("/{id_jogo}/jogador/{player_id}/verificar_objetivo")
def verificar_objetivo(id_jogo: int, player_id: int, status_atual: str):
    jogo_atual = obter_jogo(id_jogo)
    jogador = obter_jogador(jogo_atual, player_id)
    objetivo_completado = jogador.objetivo_completado(status_atual)
    
    if objetivo_completado:
        return {
            "mensagem": f"Parabéns, jogador {jogador.id}! Você completou o objetivo: {jogador.objetivo}"
        }
    else:
        return {
            "mensagem": f"Jogador {jogador.id}, você ainda não completou o objetivo: {jogador.objetivo}. Continue jogando!"
        }