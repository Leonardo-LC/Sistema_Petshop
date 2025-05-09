from packages.models.pessoa import Pessoa

class Cliente(Pessoa):

    def __init__(self,nome: str, email: str, telefone: str):
        super().__init__(nome, email, telefone)
        self.pets = []


    def __str__(self):
        return f'Cliente: {self.nome} - Telefone: {self.telefone} = Pets: {self.pets}'
