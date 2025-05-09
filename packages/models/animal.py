from abc import ABC

class Animal(ABC):

    def __init__(self, nome:str, idade: int, peso: float, tipo: str, dono):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.tipo = tipo
        self.dono = dono
        dono.pets.append(self)

    def to_dict(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "peso": self.peso,
            "tipo": self.tipo,
            # Evita referência circular: só armazena o nome do dono, não o objeto inteiro
            "dono_nome": self.dono.nome if self.dono else None
        }

    def __str__(self):
        return f'{self.nome} ({self.tipo}) - {self.idade} anos - {self.peso}kg - Dono: {self.dono.nome}'

    def __repr__(self):
        return f"Animal(nome='{self.nome}', tipo='{self.tipo}')"