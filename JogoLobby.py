import random
from Jogador import *
from Cor_exercito import *
from Objetivos import *

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

class ProxyJogador:
    def __init__(self, jogo):
        self.jogo = jogo
        self.cores = Cor_exercito()
        self.objetivos = Objetivos()

    def adicionar_jogador(self, id_jogador):
        cor = self.cores.encontra_cor()
        objetivo = self.objetivos.encontra_objetivo()

        if cor is None or objetivo is None:
            print("Não é possível adicionar o jogador. Cores ou objetivos esgotados.")
            return None

        jogador = Jogador(id_jogador, cor, objetivo)
        self.jogo.lista_jogadores[id_jogador] = jogador
        return jogador
class Jogo:

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
        self.alocacao_exercitos = {}

        self.proxyJogador = ProxyJogador(self)

    def __str__(self):
        return(f'Sou o jogo {self.id}')

    def add_jogador(self, id_jogador):
        jogador_adicionado = self.proxyJogador.adicionar_jogador(id_jogador)

        if jogador_adicionado == None:
            return False
        return True

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
        random.shuffle(territorios)
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
            jogador.exercitos = exercitos_iniciais
            self.exercitos_distribuidos[jogador_id] = exercitos_iniciais

        return self.exercitos_distribuidos
    
    def exibir_exercitos(self):
        if not self.exercitos_distribuidos:
            return "Exércitos ainda não distribuídos"
        return self.exercitos_distribuidos
    
    def alocar_exercitos(self, id_jogador, territorio, quantidade):
        if id_jogador not in self.lista_jogadores:
            return "Jogador não encontrado"
        
        jogador = self.lista_jogadores[id_jogador]
        if jogador.exercitos < quantidade:
            return "Jogador não tem exércitos suficientes para alocar"

        jogador.exercitos -= quantidade
        

        if id_jogador not in self.alocacao_exercitos:
            self.alocacao_exercitos[id_jogador] = {}

        if territorio not in self.alocacao_exercitos[id_jogador]:
            self.alocacao_exercitos[id_jogador][territorio] = 0

        self.alocacao_exercitos[id_jogador][territorio] += quantidade
        return self.alocacao_exercitos[id_jogador]

    def exibir_alocacao_exercitos(self):
        if not self.alocacao_exercitos:
            return "Nenhuma alocação de exércitos realizada"
        return self.alocacao_exercitos

    def exibir_exercitos_por_territorio(self):
        if not self.alocacao_exercitos:
            return "Nenhuma alocação de exércitos realizada"

        exercitos_por_territorio = {}

        for jogador_id, territorios in self.alocacao_exercitos.items():
            for territorio, quantidade in territorios.items():
                if territorio not in exercitos_por_territorio:
                    exercitos_por_territorio[territorio] = []
                exercitos_por_territorio[territorio].append({'jogador_id': jogador_id, 'exercitos': quantidade})

        return exercitos_por_territorio