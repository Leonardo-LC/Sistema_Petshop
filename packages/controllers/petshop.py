from packages.controllers.serializador import Serializador
from packages.models.animal import Animal
from packages.models.cliente import Cliente
from packages.models.medicovet import MedicoVet
from packages.models.gerente import Gerente
import webbrowser
import re

class Petshop:

    def __init__(self,razao_social):
        self.razao_social = razao_social
        self.clientes = Serializador("database_clientes.json")
        self.medicos = Serializador("database_medicos.json")
        self.gerentes = Serializador("database_gerentes.json")

        self.opcoes= {
            '1': self.cadastrar_cliente,
            '2': self.remover_cliente,
            #'3': self.contratar_gerente,
            #'4': self.contratar_medico,
            #'5': self.demitir_medico,
            #'6': self.mostrar_funcionarios_html,
            #'7': self.sair

        }

    def menu(self):
        output = True
        while output:
            opcao_escolhida = input("Digite o número da ação desejada: \n"
                                    "1 - Cadastrar Cliente\n"
                                    "2 - Remover Cliente\n"
                                    "3 - Contratar Gerente\n"
                                    "4 - Contratar Medico\n"
                                    "5 - Demitir Medico\n"
                                    "6 - Gerar relatório\n"
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
        nome = input('Digite o nome do cliente: ')
        nome = nome.title()

        valida_email = True
        while valida_email:
            email = input('Digite o email do cliente: ')
            if not self.validar_email(email):
                print(f'E-mail invalido! Digite um email válido.')
            else:
                valida_email = False

        valida_telefone = True
        while valida_telefone:
            telefone = input('Digite o telefone do cliente: ').strip()
            if not self.validar_telefone(telefone):
                print("Formato de telefone inválido.")
            else:
                valida_telefone = False

        #remover linha abaixo depois
        #print([cliente.telefone for cliente in self.clientes.get_models()])

        if not self.clientes.verify_number(telefone):
            cliente = Cliente(nome, telefone, email)

            quantidade = int(input("Digite quantos pets o cliente possui: "))
            for i in range(quantidade):
                nome_pet = input(f'Digite o nome do {i+1}º pet: ')
                nome_pet = nome_pet.title()
                idade = input(f'Digite a idade do pet: ')
                peso = input(f"Difite o peso do pet: ")
                tipo = input(f'Digite o tipo do animal: ')
                tipo = tipo.title()
                pet = Animal(nome_pet, int(idade), float(peso), tipo, cliente)
                #cliente.adicionar_pet(pet)

            self.clientes.adicionar_cliente(cliente)
            print(f'Cliente {cliente} adicionado com sucesso!')

        else:
            print(f'O cliente {nome} já possui cadastro no sistema!')
        return True

    def remover_cliente(self):
        nome = input(f'Digite o nome do cliente: ')
        #email = input(f"Digite o email do cliente")
        telefone = input(f'Digite o número do cliente {nome}: ')

        if self.clientes.verify_number(telefone):
            for dados in self.clientes.get_models():
                if dados["telefone"] == telefone and dados["nome"] == nome:
                    confirmacao = input(f'O(a) cliente {nome} será PERMANENTEMENTE deletado. Deseja prosseguir? S/n: ')
                    if confirmacao.lower() == 's':
                        self.clientes.get_models().remove(dados)
                        self.clientes.save()
                        print(f'O clinte {nome} foi removido com sucesso.')
                        return True
                    else:
                        print(f'Operação cancelada')
                        return True
                else:
                    print(f'{nome} não possui o telefone: {telefone}')
                    return True
        else:
            print(f'O cliente {nome} não possui cadastro no sistema')
        return True


    #Garante que o email e o telefone estejam em formato convencional

    def validar_email(self, email: str) -> bool:
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(padrao, email) is not None

    def validar_telefone(self, telefone: str) -> bool:
        padrao = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
        return re.match(padrao, telefone) is not None
