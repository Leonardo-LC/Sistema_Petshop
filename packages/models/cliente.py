from packages.models.pessoa import Pessoa
from packages.models.animal import Animal

class Cliente(Pessoa):

    def __init__(self,nome: str, email: str, telefone: str):
        super().__init__(nome, email, telefone)
        self.pets = []

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "pets": [pet.to_dict() for pet in self.pets]}

    def __str__(self):
        return f'Cliente: {self.nome} - Telefone: {self.telefone} = Pets: {self.pets}'

    def adicionar_pet(self,pet):
        self.pets.append(pet)