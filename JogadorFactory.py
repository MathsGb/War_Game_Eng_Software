from abc import ABC, abstractmethod

class JogadorFactory(ABC):
    @abstractmethod
    def criar_jogador(self, id_jogador, cor, objetivo):
        pass

class JogadorFactoryConcreto(JogadorFactory):
    def criar_jogador(self, id_jogador, cor, objetivo):
        return Jogador(id_jogador, cor, objetivo)
