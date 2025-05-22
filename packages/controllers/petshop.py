from packages.controllers.serializador import Serializador
from packages.models.animal import Animal
from packages.models.cliente import Cliente
from packages.models.medicovet import MedicoVet
from packages.models.banhista import Banhista
from packages.controllers.validadores import Validadores
from packages.controllers.valores import Valores
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
            '6': self.gerar_relatorio_html,
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
            nome = input('Digite o nome do(a) cliente: ').title()
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
                p = input(f"Difite o peso do pet: ")
                peso = p.replace(",", ".").strip()

                type = True
                while type:
                    tipo = input(f"{nome_pet} é um gato, cachorro, coelho ou hamster? ").strip().title()
                    if tipo == 'Cachorro' or tipo == 'Gato' or tipo == 'Coelho' or tipo == 'Hamster':
                        type = False
                    else:
                        print('No momento atendemos apenas cachorros,gatos, coelhos e hamsters.')

                servicos = {}
                print(f"""
Digite os serviços que serão realizados em {nome_pet}.
Digite 'fim' para encerrar.
Opções disponíveis:
- Banho
- Tosa
- Cortar unhas
- Consulta
""")

                while True:
                    servico = input("Serviço: ").strip().lower()
                    if servico == "fim":
                        break
                    elif servico in ['banho', 'tosa', 'consulta', 'cortar unhas', 'chekup']:
                        if servico in ['banho', 'tosa', 'consulta', 'cortar unhas']:
                            valor = Valores.valor_servico(servico, float(peso))
                        else:  # chekup
                            valor = Valores.valor_servico(servico)
                        servicos[servico] = valor
                    else:
                        print(f'Infelizmente o serviço {servico} ainda não está disponível.')

                pet = Animal(nome_pet, int(idade), float(peso), tipo, cliente)
                for servico, valor in servicos.items():
                    pet.contratar_servicos(servico, valor)

            self.clientes.adicionar_cliente(cliente)
            print(f'Cliente {cliente} adicionado com sucesso!')

            #print(pet.total_servicos()) teste para ver se o valor total está funcionando

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
            emaifl = input(f'Digite o email do(a) banhista {nome}: ')
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

    def gerar_relatorio_html(self):

        html_content = f"""
        <html>
        <head>
            <title>Relatório {self.razao_social}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                }}
                .container {{
                    width: 80%;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: white;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                table, th, td {{
                    border: 1px solid #ddd;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 14px;
                    color: #777;# Salvar o conteúdo HTML em um arquivo
        file_path = "relatorio.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
                }}
            </style>
        </head>
        <body>
            <h1>Relatório: {self.razao_social}</h1>
            <div class="container">
                
                <h2>Clientes</h2>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Nome</th>
                            <th>Telefone</th>
                            <th>Email</th>
                            <th>Pets</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        clientes = self.clientes.get_models()
        if clientes:
            for index, cliente in enumerate(clientes, start=1):
                html_content += f"""
                <tr>
                    <td>{index}</td>
                    <td>{cliente['nome']}</td>
                    <td>{cliente['telefone']}</td>
                    <td>{cliente['email']}</td>
                    <td>
                        <ul>
                            {"".join([
                    f"<li><strong>{pet['nome']}</strong> ({pet['tipo']}, {pet['idade']} anos, {pet['peso']}kg) - "
                    f"Serviços: {', '.join(pet['servicos_contratados'].keys())} - "
                    f"Total: R${sum(pet['servicos_contratados'].values()):.2f}</li>"
                    for pet in cliente['pets']
                ]) if cliente['pets'] else "Nenhum pet"}
                        </ul>
                    </td>
                </tr>
                """
        else:
            html_content += "<tr><td colspan='4'>Nenhum cliente cadastrado.</td></tr>"

        html_content += """
                </tbody>
                </table>
                
                <h2>Médicos</h2>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Nome</th>
                            <th>Telefone</th>
                            <th>Email</th>
                            <th>Admissão</th>
                            <th>CRMV</th>
                            <th>Salário</th>
                        </tr>
                    </thead>
                    <tbody>
        """


        medicos = self.medicos.get_models()
        if medicos:
            for index, medico in enumerate(medicos, start=1):
                html_content += f"""
                <tr>
                    <td>{index}</td>
                    <td>{medico['nome']}</td>
                    <td>{medico['telefone']}</td>
                    <td>{medico['email']}</td>
                    <td>{medico['data_admissao']}</td>
                    <td>{medico['CRMV']}</td>
                    <td>{medico['salario']}</td>
                </tr>
                """
        else:
            html_content += "<tr><td colspan='4'>Nenhum médico cadastrado.</td></tr>"


        html_content += """
                </tbody>
                </table>

                <h2>Banhistas</h2>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Nome</th>
                            <th>Residência</th>
                            <th>Email</th>
                            <th>Admissão</th>
                            <th>Salário</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        banhistas = self.banhista.get_models()
        if banhistas:
            for index, banhista in enumerate(banhistas, start=1):
                html_content += f"""
                <tr>
                    <td>{index}</td>
                    <td>{banhista['nome']}</td>
                    <td>{banhista['telefone']}</td>
                    <td>{banhista['email']}</td>
                    <td>{banhista['data_admissao']}</td>
                    <td>{banhista['salario']}</td>
                </tr>
                """
        else:
            html_content += "<tr><td colspan='4'>Nenhum banhista cadastrado.</td></tr>"

        html_content += """
                </tbody>
                </table>
            </div>
            <div class="footer">
                <p>&copy; 2024 Minha Empresa LTDA</p>
            </div>
        </body>
        </html>
        """

        file_path = "relatorio.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print("Arquivo HTML gerado com sucesso: relatorio.html")

        webbrowser.open(file_path)
        return True

