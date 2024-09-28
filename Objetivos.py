
Objetivos_padrao = {
    1: {'objetivo': 'Chegar a lua', 'disponivel': True},
    2: {'objetivo': 'Derrubar a torre Eifel', 'disponivel': True},
    3: {'objetivo': 'Conquistar a Bosnia', 'disponivel': True},
    4: {'objetivo': 'Libertar a Bosnia', 'disponivel': True},
}

class Objetivos:

    def __init__(self):
        self.objetivos =  Objetivos_padrao

    def __str__(self):
        return str(self.objetivos) 
    
    def encontra_objetivo(self):
        for i in self.objetivos:
            if self.objetivos[i]['disponivel'] == True:
                self.objetivos[i]['disponivel'] = False
                return self.objetivos[i]['objetivo']
        return None