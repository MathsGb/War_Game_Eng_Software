class Jogador:
    def __init__(self, id, cor, objetivo):
        self.id = id
        self.cor_exercito = cor
        self.objetivo = objetivo
        self.exercitos = 0
        self.territorios = {}

    def get_jogador(self):
        return [f'Jogador: {self.id}', f'cor: {self.cor_exercito}', f'objetivo: {self.objetivo}', f'exércitos: {self.exercitos}']