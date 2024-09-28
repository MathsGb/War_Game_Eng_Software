import random
from Jogador import Jogador
from Observer import Subject, Observer

lista_jogos = {}

def Cria_jogo(id):
    lista_jogos[id] = Jogo(id)

def calcula_exercitos_iniciais(num_jogadores):
    return {2: 40, 3: 35, 4: 30}.get(num_jogadores, 20)  # Melhorando legibilidade

class Jogo(Subject):
    Cores_padrao = ['vermelho', 'azul', 'amarelo', 'verde']
    
    Objetivos_padrao = [
        'Chegar a lua', 'Derrubar a torre Eifel', 
        'Conquistar a Bosnia', 'Libertar a Bosnia'
    ]

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
        return f'Sou o jogo {self.id}'

    def _encontra_cor(self):
        if self.Cores_padrao:
            return self.Cores_padrao.pop(0)
        return None
    
    def _encontra_objetivo(self):
        if self.Objetivos_padrao:
            return self.Objetivos_padrao.pop(0)
        return None

    def add_jogador(self, id_jogador):
        cor = self._encontra_cor()
        objetivo = self._encontra_objetivo()

        if not cor or not objetivo:
            print("Jogador não adicionado")
            return
        
        jogador = Jogador(id_jogador, cor, objetivo)
        self.lista_jogadores[id_jogador] = jogador
        self.add_observer(jogador)

    def add_observer(self, observer: Observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, message: str):
        for observer in self.observers:
            observer.update(message)

    def exibir_jogadores(self):
        return [jogador.get_jogador() for jogador in self.lista_jogadores.values()]

    def definir_ordem_jogadores(self):
        self.ordem_jogadores = list(self.lista_jogadores.keys())
        random.shuffle(self.ordem_jogadores)
        return self.ordem_jogadores

    def get_ordem_jogadores(self):
        return self.ordem_jogadores or "Ordem dos jogadores ainda não definida"

    def distribuir_territorios(self):
        territorios = random.sample(self.TERRITORIOS, len(self.TERRITORIOS))
        jogadores_ids = list(self.lista_jogadores.keys())
        num_jogadores = len(jogadores_ids)
        
        if not num_jogadores:
            return "Nenhum jogador para distribuir territórios"

        distribuicao = {jogador_id: [] for jogador_id in jogadores_ids}
        for i, territorio in enumerate(territorios):
            distribuicao[jogadores_ids[i % num_jogadores]].append(territorio)

        self.territorios_distribuidos = distribuicao
        return distribuicao

    def exibir_territorios(self):
        return self.territorios_distribuidos or "Territórios ainda não distribuídos"

    def distribuir_exercitos(self):
        num_jogadores = len(self.lista_jogadores)
        if not num_jogadores:
            return "Nenhum jogador para distribuir exércitos"
        
        exercitos_iniciais = calcula_exercitos_iniciais(num_jogadores)
        for jogador in self.lista_jogadores.values():
            jogador.exercitos = exercitos_iniciais
        self.exercitos_distribuidos = {jogador_id: jogador.exercitos for jogador_id, jogador in self.lista_jogadores.items()}

        return self.exercitos_distribuidos
    
    def exibir_exercitos(self):
        return self.exercitos_distribuidos or "Exércitos ainda não distribuídos"
    
    def alocar_exercitos(self, id_jogador, territorio, quantidade):
        jogador = self.lista_jogadores.get(id_jogador)
        if not jogador:
            return "Jogador não encontrado"
        
        if jogador.exercitos < quantidade:
            return "Jogador não tem exércitos suficientes para alocar"

        jogador.exercitos -= quantidade

        self.alocacao_exercitos.setdefault(id_jogador, {})
        self.alocacao_exercitos[id_jogador].setdefault(territorio, 0)
        self.alocacao_exercitos[id_jogador][territorio] += quantidade

        return self.alocacao_exercitos[id_jogador]

    def exibir_alocacao_exercitos(self):
        return self.alocacao_exercitos or "Nenhuma alocação de exércitos realizada"

    def exibir_exercitos_por_territorio(self):
        exercitos_por_territorio = {}
        for jogador_id, territorios in self.alocacao_exercitos.items():
            for territorio, quantidade in territorios.items():
                exercitos_por_territorio.setdefault(territorio, []).append({'jogador_id': jogador_id, 'exercitos': quantidade})
        return exercitos_por_territorio or "Nenhuma alocação de exércitos realizada"

    def verificar_objetivo(self, id_jogador, status_atual):
        jogador = self.lista_jogadores.get(id_jogador)
        if not jogador:
            return "Jogador não encontrado"
        
        if jogador.objetivo_completado():
            self.notify_observers(f"O jogador {jogador.id} completou seu objetivo!")
            return True
        return False