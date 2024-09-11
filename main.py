from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import random

app = FastAPI()

lista_jogos = {}

def Cria_jogo(id):
    lista_jogos[id] = Jogo(id)

def calcula_exercitos_iniciais(num_jogadores):
    if num_jogadores == 2:
        return 40
    elif num_jogadores == 3:
        return 35
    elif num_jogadores == 4:
        return 30
    else:
        return 20  

class Jogo:
    Cores_padrao = {
        1: {'cor': 'vermelho', 'disponivel': True},
        2: {'cor': 'azul', 'disponivel': True},
        3: {'cor': 'amarelo', 'disponivel': True},
        4: {'cor': 'verde', 'disponivel': True},
    }
    
    Objetivos_padrao = {
        1: {'objetivo': 'Chegar a lua', 'disponivel': True},
        2: {'objetivo': 'Derrubar a torre Eifel', 'disponivel': True},
        3: {'objetivo': 'Conquistar a Bosnia', 'disponivel': True},
        4: {'objetivo': 'Libertar a Bosnia', 'disponivel': True},
    }

    TERRITORIOS = [
        'Território 1', 'Território 2', 'Território 3', 'Território 4',
        'Território 5', 'Território 6', 'Território 7', 'Território 8'
    ]

    def __init__(self, id):
        self.id = id
        self.lista_jogadores = {}
        self.ordem_jogadores = []
        self.territorios_distribuidos = {}
        self.exercitos_distribuidos = {}

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

    def definir_ordem_jogadores(self):
        ids_jogadores = list(self.lista_jogadores.keys())
        random.shuffle(ids_jogadores)  
        self.ordem_jogadores = ids_jogadores  
        return self.ordem_jogadores

    def get_ordem_jogadores(self):
        if not self.ordem_jogadores:
            return "Ordem dos jogadores ainda não definida"
        return self.ordem_jogadores

    def distribuir_territorios(self):
        territorios = self.TERRITORIOS.copy()
        random.shuffle(territorios)  # Embaralha a lista de territórios
        jogadores_ids = list(self.lista_jogadores.keys())
        num_jogadores = len(jogadores_ids)
        
        if num_jogadores == 0:
            return "Nenhum jogador para distribuir territórios"

        territorios_por_jogador = len(territorios) // num_jogadores
        distribuicao = {jogador_id: [] for jogador_id in jogadores_ids}

        for i, territorio in enumerate(territorios):
            jogador_id = jogadores_ids[i % num_jogadores]
            distribuicao[jogador_id].append(territorio)

        self.territorios_distribuidos = distribuicao
        return distribuicao

    def exibir_territorios(self):
        if not self.territorios_distribuidos:
            return "Territórios ainda não distribuídos"
        return self.territorios_distribuidos

    def distribuir_exercitos(self):
        num_jogadores = len(self.lista_jogadores)
        if num_jogadores == 0:
            return "Nenhum jogador para distribuir exércitos"
        
        exercitos_iniciais = calcula_exercitos_iniciais(num_jogadores)
        for jogador_id, jogador in self.lista_jogadores.items():
            jogador.exercitos = exercitos_iniciais  # Salva o número de exércitos no jogador
            self.exercitos_distribuidos[jogador_id] = exercitos_iniciais

        return self.exercitos_distribuidos
    
    def exibir_exercitos(self):
        if not self.exercitos_distribuidos:
            return "Exércitos ainda não distribuídos"
        return self.exercitos_distribuidos

class Jogador:
    def __init__(self, id, cor, objetivo):
        self.id = id
        self.cor_exercito = cor
        self.objetivo = objetivo
        self.exercitos = 0

    def get_jogador(self):
        return [f'Jogador: {self.id}', f'cor: {self.cor_exercito}', f'objetivo: {self.objetivo}', f'exércitos: {self.exercitos}']

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
        return {1: {f'Você agora está dentro de um jogo de número {jogo_atual.id}'},
                2: {f'Atualmente tenho {len(jogo_atual.lista_jogadores)} jogadores presentes'},
                3: {f'Os jogadores atualmente são: {jogo_atual.exibir_jogadores()}'}
                }
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