
from Observer import Observer

class Jogador(Observer):
    def __init__(self, id, cor, objetivo):
        self.id = id
        self.cor = cor
        self.objetivo = objetivo
        self.exercitos = 0
    
    def get_jogador(self):
        return {'id': self.id, 'cor': self.cor, 'objetivo': self.objetivo}

    def update(self, message: str):
        print(f"Jogador {self.id} notificado: {message}")

    def objetivo_completado(self, status_atual):
        # Lógica que verifica se o objetivo foi completado
        if status_atual == "objetivo completado":
            return True
        return False