from packages.models.funcionario import Funcionario
from datetime import date

class Gerente(Funcionario):
    def __init__(self,salario: float, data_admissao: date, nome: str, email: str, telefone: str):
        super().__init__(salario, data_admissao, nome, email, telefone)

    def __str__(self):
        return f'Gerente: {self.nome}'
