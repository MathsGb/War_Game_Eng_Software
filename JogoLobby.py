class Jogo:
    _instances = {}

    def __new__(cls, id_jogo, *args, **kwargs):
        if id_jogo not in cls._instances:
            instance = super(Jogo, cls).__new__(cls)
            cls._instances[id_jogo] = instance
        return cls._instances[id_jogo]

    def __init__(self, id_jogo):
        if not hasattr(self, "inicializado"):  # Para evitar a reinicialização
            self.id = id_jogo
            self.lista_jogadores = []
            self.territorios = []
            self.exercitos = []
            self.inicializado = True

    def add_jogador(self, player_id):
        self.lista_jogadores.append(player_id)

    def exibir_jogadores(self):
        return self.lista_jogadores

    def definir_ordem_jogadores(self):
        self.ordem_jogadores = sorted(self.lista_jogadores)
        return self.ordem_jogadores

    def get_ordem_jogadores(self):
        return self.ordem_jogadores if hasattr(self, 'ordem_jogadores') else []

    def distribuir_territorios(self):
        # Lógica de distribuição dos territórios
        self.territorios = ["Território 1", "Território 2"]  # Exemplo
        return self.territorios

    def exibir_territorios(self):
        return self.territorios

    def distribuir_exercitos(self):
        # Lógica de distribuição dos exércitos
        self.exercitos = {"Território 1": 10, "Território 2": 15}
        return self.exercitos

    def exibir_exercitos(self):
        return self.exercitos

    def alocar_exercitos(self, player_id, territorio, quantidade):
        # Lógica para alocar exércitos
        if territorio in self.exercitos:
            self.exercitos[territorio] += quantidade
        else:
            self.exercitos[territorio] = quantidade
        return f"{quantidade} exércitos alocados para {territorio}"

    def exibir_alocacao_exercitos(self):
        return self.exercitos

    def exibir_exercitos_por_territorio(self):
        return self.exercitos
