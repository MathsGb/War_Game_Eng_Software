from Observer import Observer

class Jogador(Observer):
    def __init__(self, id, cor, objetivo):
        self.id = id
        self.cor = cor
        self.objetivo = objetivo
        self.exercitos = 0
        self.territorios_controlados = []
    
    def get_jogador(self):
        return {'id': self.id, 'cor': self.cor, 'objetivo': self.objetivo}

    def update(self, message: str):
        print(f"Jogador {self.id} notificado: {message}")

    def adicionar_territorio(self, territorio):
        self.territorios_controlados.append(territorio)

    def objetivo_completado(self):
        return any(territorio == self.objetivo for territorio in self.territorios_controlados)
