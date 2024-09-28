import random
from Jogador import Jogador
from Observer import Subject, Observer

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

class Jogo(Subject):
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
        self.observers = []
        self.ordem_jogadores = []
        self.territorios_distribuidos = {}
        self.exercitos_distribuidos = {}
        self.alocacao_exercitos = {}

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
        jogador = Jogador(id_jogador, cor, objetivo)
        self.lista_jogadores[id_jogador] = jogador
        self.add_observer(jogador)

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observers(self, message: str):
        for observer in self.observers:
            observer.update(message)

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

    def verificar_objetivo(self, id_jogador, status_atual):
        if id_jogador not in self.lista_jogadores:
            return "Jogador não encontrado"
        
        jogador = self.lista_jogadores[id_jogador]
        if jogador.objetivo_completado(status_atual):
            self.notify_observers(f"O jogador {jogador.id} completou seu objetivo!")
            return True
        return False
