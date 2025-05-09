from abc import ABC

class Animal(ABC):

    def __init__(self, nome:str, idade: int, peso: float, tipo: str, dono):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.tipo = tipo
        self.dono = dono
        dono.pets.append(self)

    def __str__(self):
        return f'{self.nome} ({self.tipo}) - {self.idade} anos - {self.peso}kg - Dono: {self.dono.nome}'
