from datetime import date
from packages.pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(self,nome:str, telefone:str, email:str, cpf: str, turno: str, data_admissao: date,
                 salario: float, departamento: str, nivel_acesso: int):

        super().__init__(nome, telefone, email)
        self.__cpf = cpf
        self.turno = turno
        self.data_admissao = data_admissao
        self.__salario = salario
        self.departamento = departamento
        self.__nivel_acesso = nivel_acesso

