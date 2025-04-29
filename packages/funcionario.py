class Funcionario:
    def __init__(self, cpf: str, turno: str, data_admissao: date,
                 salario: float, departamento: str, nivel_acesso: int):

        self.__cpf = cpf
        self.turno = turno
        self.data_admissao = data_admissao
        self.__salario = salario
        self.departamento = departamento
        self.__nivel_acesso = nivel_acesso