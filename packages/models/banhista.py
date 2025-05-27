from packages.models.funcionario import Funcionario
from datetime import date

class Banhista(Funcionario):
    def __init__(self, nome: str, email: str, telefone: str, salario: float, data_admissao: date):
        super().__init__(salario, data_admissao, nome, email, telefone)
        #self.agenda_banhista = []

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "salario": self.salario,
            "data_admissao": self.data_admissao
        }

    def __str__(self):
        return f'Banhista: {self.nome}'
