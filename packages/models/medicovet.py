from packages.models.funcionario import Funcionario
from datetime import date

class MedicoVet(Funcionario):

    def __init__(self, nome: str, email: str, telefone: str, salario: float, data_admissao: date, crmv: str):
        super().__init__(salario, data_admissao, nome, email, telefone)
        self.crmv = crmv
        #self.agenda_medico = []

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "salario": self.salario,
            "data_admissao": self.data_admissao,
            "CRMV": self.crmv
        }

    def __str__(self):

        return f'Médico: {self.nome} - CRMV: {self.crmv}'
