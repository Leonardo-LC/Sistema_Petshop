from tkinter import *
from tkinter import ttk, messagebox
from packages.controllers.serializador import Serializador
from packages.models.cliente import Cliente
from packages.models.animal import Animal
from packages.controllers.validadores import Validadores
import re


class PetshopInterface:
    def __init__(self, root):
        self.root = root
        self.configurar_janela()
        self.criar_widgets()
        self.serializador = Serializador("database_clientes.json")
        self.carregar_clientes()

    def configurar_janela(self):
        self.root.title("Sistema Petshop")
        self.root.geometry("1200x600")  # Aumentei o tamanho para caber mais colunas
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)

    def criar_widgets(self):
        # Frame principal
        self.main_frame = Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Frame de formulário
        self.form_frame = LabelFrame(self.main_frame, text="Cadastro de Clientes e Pets",
                                     bg='#f0f0f0', fg='#333', font=('Arial', 10, 'bold'))
        self.form_frame.pack(fill=X, padx=5, pady=5)

        # Campos do cliente (lado esquerdo)
        labels_cliente = ['Nome*:', 'Telefone*:', 'Email*:']
        entries_cliente = ['nome_entry', 'telefone_entry', 'email_entry']

        for i, (label, entry) in enumerate(zip(labels_cliente, entries_cliente)):
            Label(self.form_frame, text=label, bg='#f0f0f0').grid(row=i, column=0, sticky=W, padx=5, pady=2)
            setattr(self, entry, Entry(self.form_frame, width=30))
            getattr(self, entry).grid(row=i, column=1, padx=5, pady=2)

        # Campos do pet (lado direito)
        labels_pet = ['Nome Pet*:', 'Idade*:', 'Peso (kg)*:', 'Tipo*:', 'Serviços (separados por vírgula):']
        entries_pet = ['nome_pet_entry', 'idade_entry', 'peso_entry', 'tipo_entry', 'servicos_entry']

        for i, (label, entry) in enumerate(zip(labels_pet, entries_pet)):
            Label(self.form_frame, text=label, bg='#f0f0f0').grid(row=i, column=2, sticky=W, padx=5, pady=2)
            setattr(self, entry, Entry(self.form_frame, width=30))
            getattr(self, entry).grid(row=i, column=3, padx=5, pady=2)

        # Botões
        botoes = [
            ('Limpar', self.limpar_campos, '#d9534f'),
            ('Adicionar', self.adicionar_cliente_pet, '#5cb85c'),
            ('Remover', self.remover_cliente, '#d9534f')
        ]

        btn_frame = Frame(self.form_frame, bg='#f0f0f0')
        btn_frame.grid(row=5, columnspan=4, pady=10)

        for text, command, color in botoes:
            Button(btn_frame, text=text, bg=color, fg='white',
                   command=command).pack(side=LEFT, padx=5)

        # Lista de clientes (Treeview)
        self.lista_frame = LabelFrame(self.main_frame, text="Clientes e Pets Cadastrados",
                                      bg='#f0f0f0', fg='#333', font=('Arial', 10, 'bold'))
        self.lista_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        colunas = ['Nome', 'Telefone', 'Email', 'Pet', 'Tipo', 'Idade', 'Peso', 'Serviços', 'Total']
        self.tree = ttk.Treeview(self.lista_frame, columns=colunas, show='headings')

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind('<Double-1>', self.preencher_campos)

        # Scrollbar
        scroll = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def limpar_campos(self):
        for entry in [self.nome_entry, self.telefone_entry, self.email_entry,
                      self.nome_pet_entry, self.idade_entry, self.peso_entry,
                      self.tipo_entry, self.servicos_entry]:
            entry.delete(0, END)

    def carregar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        clientes = self.serializador.get_models()
        for cliente in clientes:
            if cliente['pets']:
                for pet in cliente['pets']:
                    total = sum(pet['servicos_contratados'].values()) if pet['servicos_contratados'] else 0
                    servicos = ", ".join(pet['servicos_contratados'].keys()) if pet['servicos_contratados'] else ""

                    self.tree.insert('', END, values=(
                        cliente['nome'],
                        cliente['telefone'],
                        cliente['email'],
                        pet['nome'],
                        pet['tipo'],
                        pet['idade'],
                        pet['peso'],
                        servicos,
                        f"R$ {total:.2f}"
                    ))
            else:
                self.tree.insert('', END, values=(
                    cliente['nome'],
                    cliente['telefone'],
                    cliente['email'],
                    "", "", "", "", "", ""
                ))

    def preencher_campos(self, event):
        self.limpar_campos()
        item = self.tree.selection()[0]
        valores = self.tree.item(item, 'values')

        self.nome_entry.insert(0, valores[0])
        self.telefone_entry.insert(0, valores[1])
        self.email_entry.insert(0, valores[2])
        self.nome_pet_entry.insert(0, valores[3])
        self.tipo_entry.insert(0, valores[4])
        self.idade_entry.insert(0, valores[5])
        self.peso_entry.insert(0, valores[6])
        self.servicos_entry.insert(0, valores[7])

    def validar_campos(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        nome_pet = self.nome_pet_entry.get()
        idade = self.idade_entry.get()
        peso = self.peso_entry.get()
        tipo = self.tipo_entry.get()

        if not nome or not Validadores.validar_nome(self, nome):
            messagebox.showerror("Erro", "Nome inválido! Deve ter pelo menos 3 caracteres.")
            return False

        if not telefone or not Validadores.validar_telefone(self, telefone):
            messagebox.showerror("Erro", "Telefone inválido! Formato esperado: (XX)XXXXX-XXXX")
            return False

        if not email or not Validadores.validar_email(self, email):
            messagebox.showerror("Erro", "Email inválido! Formato esperado: usuario@dominio.com")
            return False

        if nome_pet and (not idade or not peso or not tipo):
            messagebox.showerror("Erro",
                                 "Para cadastrar um pet, todos os campos (Nome, Idade, Peso e Tipo) devem ser preenchidos!")
            return False

        return True

    def adicionar_cliente_pet(self):
        if not self.validar_campos():
            return

        # Verifica se o cliente já existe
        clientes = self.serializador.get_models()
        cliente_existente = next((c for c in clientes if c['telefone'] == self.telefone_entry.get()), None)

        if cliente_existente:
            cliente = Cliente(
                nome=cliente_existente['nome'],
                email=cliente_existente['email'],
                telefone=cliente_existente['telefone']
            )
            # Carrega os pets existentes
            cliente.pets = [pet for pet in cliente_existente['pets']]
        else:
            cliente = Cliente(
                nome=self.nome_entry.get(),
                telefone=self.telefone_entry.get(),
                email=self.email_entry.get()
            )

        # Adiciona o pet se os campos estiverem preenchidos
        nome_pet = self.nome_pet_entry.get()
        if nome_pet:
            try:
                idade = int(self.idade_entry.get())
                peso = float(self.peso_entry.get())
                tipo = self.tipo_entry.get()
                servicos = [s.strip() for s in self.servicos_entry.get().split(',') if s.strip()]

                # Cria o pet
                pet = Animal(
                    nome=nome_pet,
                    idade=idade,
                    peso=peso,
                    tipo=tipo,
                    dono=cliente
                )

                # Adiciona serviços com valores padrão (poderia ser ajustado para pedir os valores)
                for servico in servicos:
                    valor = 50.0  # Valor padrão, poderia ser um input adicional
                    pet.contratar_servicos(servico, valor)

                cliente.adicionar_pet(pet)

            except ValueError:
                messagebox.showerror("Erro", "Idade e Peso devem ser números válidos!")
                return

        # Adiciona ou atualiza o cliente
        if cliente_existente:
            # Remove o cliente antigo para adicionar o atualizado
            self.serializador.remover_cliente(cliente)

        self.serializador.adicionar_cliente(cliente)
        self.carregar_clientes()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

    def remover_cliente(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione um cliente para remover!")
            return

        valores = self.tree.item(item_selecionado[0], 'values')

        if messagebox.askyesno("Confirmar", "Deseja realmente remover este cliente e seus pets?"):
            clientes = self.serializador.get_models()
            clientes[:] = [c for c in clientes if c['telefone'] != valores[1]]
            self.serializador.save()
            self.carregar_clientes()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")


if __name__ == "__main__":
    root = Tk()
    app = PetshopInterface(root)
    root.mainloop()