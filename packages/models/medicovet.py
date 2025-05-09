from packages.models.funcionario import Funcionario
from datetime import date

class MedicoVet(Funcionario):

    def __init__(self,crmv: str, salario: float, data_admissao: date, nome: str, email: str, telefone: str ):
        super().__init__(salario, data_admissao, nome, email, telefone)
        self.crmv = crmv

    def __str__(self):

        return f'Médico: {self.nome} - CRMV: {self.crmv}'
