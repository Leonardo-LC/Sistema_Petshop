from packages.models.pessoa import Pessoa
from datetime import date

class Funcionario(Pessoa):

    def __init__(self, salario: float, data_admissao: date, nome, email, telefone):
        super().__init__(nome, telefone, email)
        self.salario = salario
        self.data_admissao = data_admissao

