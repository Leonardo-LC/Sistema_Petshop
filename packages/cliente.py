from packages.pessoa import Pessoa

class Cliente(Pessoa):
    def __init__(self, nome:str, telefone:str, email: str, animal: str, pet: str):
        super().__init__(nome, telefone, email)
        self.pet = pet

