from packages.funcionario import Funcionario
from datetime import date

class Balconista(Funcionario):
    def __init__(self, nome: str, telefone: str, email: str,
                 cpf: str, turno: str, data_admissao: date,
                 salario: float, departamento: str, nivel_acesso: int):

        super().__init__(nome, telefone, email, cpf, turno,
                         data_admissao, salario, departamento, nivel_acesso)

