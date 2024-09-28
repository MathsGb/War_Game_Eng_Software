
Cores_padrao = {
    1: {'cor': 'vermelho', 'disponivel': True},
    2: {'cor': 'azul', 'disponivel': True},
    3: {'cor': 'amarelo', 'disponivel': True},
    4: {'cor': 'verde', 'disponivel': True},
}

class Cor_exercito:
    def __init__(self):
        self.cores =  Cores_padrao
    
    def __str__(self):
        return str(self.cores)
    
    def encontra_cor(self):
        for i in self.cores:
            if self.cores[i]['disponivel'] == True:
                self.cores[i]['disponivel'] = False
                return self.cores[i]['cor']
        return None
