from packages.controllers.serializador import Serializador
from packages.models.animal import Animal
from packages.models.cliente import Cliente
from packages.models.medicovet import MedicoVet
from packages.models.banhista import Banhista
from packages.controllers.validadores import Validadores
import webbrowser
from datetime import datetime


class Petshop:

    def __init__(self,razao_social):
        self.razao_social = razao_social
        self.clientes = Serializador("database_clientes.json")
        self.medicos = Serializador("database_medicos.json")
        self.banhista = Serializador("database_banhistas.json")

        self.opcoes= {
            '1': self.cadastrar_cliente,
            '2': self.remover_cliente,
            '3': self.contratar_banhista,
            '4': self.contratar_medico,
            '5': self.demitir_funcionario,
            #'6': self.gerar_relatorio_html,
            '7': self.sair

        }

    def menu(self):
        output = True
        while output:
            opcao_escolhida = input("Digite o número da ação desejada: \n"
                                    "1 - Agendar Cliente\n"
                                    "2 - Remover Cliente\n"
                                    "3 - Contratar Banhista\n"
                                    "4 - Contratar Medico\n"
                                    "5 - Demitir Funcionário\n"
                                    "6 - Gerar Relatório\n"
                                    "7 - Sair\n"
                                    "Digite aqui: ")
            output = self.opcoes.get(opcao_escolhida, self.default)()

    def default(self):
        print('Escolha uma dos números listados nas opçãos abaixo:')
        return True

    def sair(self):
        print(f'Desligando programa...')
        return False

    def cadastrar_cliente(self):

        valida_nome = True
        while valida_nome:
            nome = input('Digite o nome do(a) cliente: ')
            if not Validadores.validar_nome(self,nome):
                print('Nome inválido.')
            else:
                valida_nome = False

        valida_email = True
        while valida_email:
            email = input(f'Digite o email do(a) cliente {nome}: ')
            if not Validadores.validar_email(self,email):
                print(f'E-mail invalido! Digite um email válido.')
            else:
                valida_email = False

        valida_telefone = True
        while valida_telefone:
            telefone = input(f'Digite o telefone do(a) cliente {nome}: ').strip()
            if not Validadores.validar_telefone(self,telefone):
                print("Formato de telefone inválido.")
            else:
                valida_telefone = False

        #remover linha abaixo depois
        #print([cliente.telefone for cliente in self.clientes.get_models()])

        if not self.clientes.verify_number(telefone):
            cliente = Cliente(nome, telefone, email)

            quantidade = int(input(f"Digite quantos pets o(a) cliente {nome} possui: "))
            for i in range(quantidade):
                nome_pet = input(f'Digite o nome do {i+1}º pet: ').title()
                idade = input(f'Digite a idade do pet: ')
                peso = input(f"Difite o peso do pet: ")

                type = True
                while type:
                    tipo = input(f"{nome_pet} é um gato, cachorro, coelho ou hamster? ").strip().title()
                    if tipo == 'Cachorro' or tipo == 'Gato' or tipo == 'Coelho' or tipo == 'Hamster':
                        type = False
                    else:
                        print('No momento atendemos apenas cachorros,gatos, coelhos e hamsters.')

                servicos = []
                print(f"""
                Digite os serviços que serão realizados em {nome_pet}.
                Digite 'fim' para encerrar.
                Opções disponíveis:
                - Banho
                - Tosa
                - Cortar unhas
                - Consulta
                - Check-up
                """)

                while True:
                    servico = input("Serviço: ").title().strip()
                    if servico.lower() == "fim":
                        break
                    if servico == 'Banho' or servico == 'Tosa' or servico == 'Consulta' or servico == 'Cortar unhas':
                        servicos.append(servico)
                    else:
                        print(f'Infelizmente o serviço {servico} ainda não está diponível.')

                pet = Animal(nome_pet, int(idade), float(peso), tipo, cliente)
                for servico in servicos:
                    pet.contratar_servicos(servico)

            self.clientes.adicionar_cliente(cliente)
            print(f'Cliente {cliente} adicionado com sucesso!')

        else:
            print(f'O(A) cliente {nome} já possui cadastro no sistema!')
        return True

    def remover_cliente(self):
        nome = input(f'Digite o nome do(a) cliente: ').title()
        telefone = input(f'Digite o número do(a) cliente {nome}: ')

        if self.clientes.verify_number(telefone):
            for dados in self.clientes.get_models():
                if dados["telefone"] == telefone and dados["nome"] == nome:
                    confirmacao = input(f'O(a) cliente {nome} será PERMANENTEMENTE deletado(a). Deseja prosseguir? S/n: ')
                    if confirmacao.lower() == 's':
                        self.clientes.get_models().remove(dados)
                        self.clientes.save()
                        print(f'O cliente {nome} foi removido(a) com sucesso.')
                        return True
                    else:
                        print(f'Operação cancelada')
                        return True
                else:
                    print(f'{nome} não possui o telefone: {telefone}')
                    return True
        else:
            print(f'O(a) cliente {nome} não possui cadastro no sistema')
        return True

    def contratar_banhista(self):
        nome = input('Digite o nome do(a) banhista: ').title()

        valida_email = True
        while valida_email:
            email = input(f'Digite o email do(a) banhista {nome}: ')
            if not Validadores.validar_email(self, email):
                print(f'E-mail invalido! Digite um email válido.')
            else:
                valida_email = False

        valida_telefone = True
        while valida_telefone:
            telefone = input(f'Digite o telefone do(a) banhista {nome}: ').strip()
            if not Validadores.validar_telefone(self,telefone):
                print("Formato de telefone inválido.")
            else:
                valida_telefone = False

        salario = float(input(f'Digite o salario do(a) banhista: '))
        data_admissao = datetime.now().strftime('%d/%m/%y')
        banhista = Banhista(nome, email, telefone, salario, data_admissao)
        self.banhista.contratar(banhista)
        print(f'O(a) banhista {nome} foi contratado com sucesso!')
        return True

    def contratar_medico(self):
        nome = input('Digite o nome do(a) médico(a): ').title()

        valida_email = True
        while valida_email:
            email = input(f'Digite o email do(a) médico(a) {nome}: ')
            if not Validadores.validar_email(self,email):
                print(f'E-mail invalido! Digite um email válido.')
            else:
                valida_email = False

        valida_telefone = True
        while valida_telefone:
            telefone = input(f'Digite o telefone do(a) médico(a) {nome}: ').strip()
            if not Validadores.validar_telefone(self,telefone):
                print("Formato de telefone inválido.")
            else:
                valida_telefone = False

        crmv = input(f'Digite a CRMV do(a) médico(a) {nome}: ')
        salario = float(input(f'Digite o salario do(a) médico(a): '))
        data_admissao = datetime.now().strftime('%d/%m/%y')
        medico = MedicoVet(nome, email, telefone, salario, data_admissao, crmv)
        self.medicos.contratar(medico)
        print(f'O(a) médico(a) {nome} foi contratado com sucesso!')
        return True

    def demitir_funcionario(self):
        nome = input('Digite o nome do(a) funcionário(a) a ser demitido: ').title()
        telefone = input(f'Digite o telefone do(a) funcionário(a) {nome}: ')

        categorias = [("banhista", self.banhista), ("médico", self.medicos)]

        for cargo, modelo in categorias:
            for dados in modelo.get_models():
                if dados["nome"] == nome and dados["telefone"] == telefone:
                    confirmacao = input(
                        f'O(a) {cargo} {nome} será demitido(a) e permanentemente removido do sistema. Deseja prosseguir? (S/n): '
                    ).lower()

                    if confirmacao == 's':
                        modelo.get_models().remove(dados)
                        modelo.save()
                        print(f'O(a) {cargo} {nome} foi demitido(a).')
                    else:
                        print('Operação cancelada.')
                    return True

        print('Funcionário(a) não encontrado.')
        return True



    #Garante que o email e o telefone estejam em formato convencional

    #def validar_email(self, email: str) -> bool:
    #    padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    #    return re.match(padrao, email) is not None

    #def validar_telefone(self, telefone: str) -> bool:
    #    padrao = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
    #    return re.match(padrao, telefone) is not None

    #def validar_nome(self, nome: str) -> bool:
    #    padrao = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+$'
    #    return re.match(padrao, nome) is not None and len(nome.strip()) >= 3