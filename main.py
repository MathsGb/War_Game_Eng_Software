from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

lista_jogos = {}

def Cria_jogo(id):
    lista_jogos[id] = Jogo(id)

class Jogo:
    Cores_padrao = {
    1: {'cor': 'vermelho' , 'disponivel': True},
    2: {'cor': 'azul', 'disponivel': True},
    3: {'cor': 'amarelo', 'disponivel': True},
    4: {'cor': 'verde' , 'disponivel': True},
    }
    
    Objetivos_padrao = {
        1: {'objetivo': 'Chegar a lua', 'disponivel': True},
        2: {'objetivo': 'Derrubar a torre Eifel', 'disponivel': True},
        3: {'objetivo': 'Conquistar a Bosnia', 'disponivel': True},
        4: {'objetivo': 'Libertar a Bosnia', 'disponivel': True},
    }

    def __init__(self, id):
        self.id = id
        self.lista_jogadores = {}

    def __str__(self):
        return(f'Sou o jogo {self.id}')

    def encontra_cor(self):
        for i in self.Cores_padrao:
            if self.Cores_padrao[i]['disponivel'] == True:
                self.Cores_padrao[i]['disponivel'] = False
                return self.Cores_padrao[i]['cor']
        return None
    
    def encontra_objetivo(self):
        for i in self.Objetivos_padrao:
            if self.Objetivos_padrao[i]['disponivel'] == True:
                self.Objetivos_padrao[i]['disponivel'] = False
                return self.Objetivos_padrao[i]['objetivo']
        return None

    def add_jogador(self, id_jogador):
        cor = self.encontra_cor()
        objetivo = self.encontra_objetivo()

        if cor == None or objetivo == None:
            return print("Jogador não adicionado")
        self.lista_jogadores[id_jogador] = Jogador(id_jogador, cor, objetivo)

    def exibir_jogadores(self):
        msg = []
        for i in self.lista_jogadores:
            player_atual = self.lista_jogadores[i]
            msg.append(player_atual.get_jogador())
        return msg

class Jogador:
    def __init__(self, id , cor, objetivo):
        self.id = id
        self.cor_exercito = cor
        self.objetivo = objetivo

    def get_jogador(self):
        return [f'Jogador: {self.id}',f'cor: {self.cor_exercito}',f'objetivo: {self.objetivo}']

#----------- rotas ---------------

@app.get("/")
def home():
    return {"Olá": "Vamos começar!",
            "Atualmente há:": f"{len(lista_jogos)} jogos"}

@app.get("/create/{id_novo_jogo}")
def novo_jogo(id_novo_jogo: int):
    Cria_jogo(id_novo_jogo)
    return RedirectResponse(url="/")

@app.get("/{id_jogo}")
def jogo_lobby(id_jogo: int):
    try:
        jogo_atual = lista_jogos[id_jogo]
        return {1: {f'Voce agora está dentro de um jogo de número {jogo_atual.id}'},
                2: {f'Atualmente tenho {len(jogo_atual.lista_jogadores)} jogadores presentes'},
                3: {f'Os jogadores atualmente são: {jogo_atual.exibir_jogadores()}'}
                }
    except KeyError:
        return RedirectResponse(url="/")

@app.get("/{id_jogo}/add/{player_id}")
def adiciona_player(id_jogo: int, player_id: int):
    jogo_atual = lista_jogos[id_jogo]
    jogo_atual.add_jogador(player_id)
    return {'jogador adicionado com sucesso'}