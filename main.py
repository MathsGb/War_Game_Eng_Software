from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

lista_jogos = {

}

Cores_padrao = {
    1: {'cor': 'vermelho'},
    2: {'cor': 'azul'},
    3: {'cor': 'amarelo'},
    4: {'cor': 'verde'}
}

Objetivos_padrao = {
    1: {'objetivo': 'Chegar a lua'},
    2: {'objetivo': 'Derrubar a torre Eifel'},
    3: {'objetivo': 'Conquistar a Bosnia'},
    4: {'objetivo': 'Libertar a Bosnia'},
}

def Cria_jogo(id):
    lista_jogos[id]= Jogo(id)

# def return_jogo(id):
#     return lista_jogos

class Jogo:
    def __init__(self, id):
        self.id = id
        self.lista_jogadores = []

    def get_id_jogo(self):
        return self.id
    
    def add_jogador(self, jogador):
        self.lista_jogadores.append(jogador)
        # jogador.objetivo = set_objetivo()

    # def adiciona_jogador(jogador_id):

class Jogador:
    cor: str
    objetivo: str
    frota = {
        1: {'Pais': 'Bosnia' , 'Exercitos': '4'},
    }

@app.get("/")
def home():
    return {"Hello": "Vamos começar!",
            "Atualmente há:": f"{len(lista_jogos)} jogos",}

@app.get("/create/{id_novo_jogo}")
def new_game(id_novo_jogo: int):
    Cria_jogo(id_novo_jogo)
    return RedirectResponse(url="/")

@app.get("/{id_jogo}")
def jogo_lobby(id_jogo: int):
    if(lista_jogos[id_jogo] == None):
        return 
    jogo_atual = lista_jogos[id_jogo]
    return {f'Voce agora está dentro de um jogo de número {jogo_atual.id}',
            f'Atualmente tenho {len(jogo_atual.lista_jogadores)} jogadores presentes'}

