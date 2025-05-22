from tkinter import *
from tkinter import ttk, messagebox
from packages.controllers.serializador import Serializador
from packages.models.cliente import Cliente
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
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)

    def criar_widgets(self):
        # Frame principal
        self.main_frame = Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Frame de formulário
        self.form_frame = LabelFrame(self.main_frame, text="Cadastro de Clientes",
                                     bg='#f0f0f0', fg='#333', font=('Arial', 10, 'bold'))
        self.form_frame.pack(fill=X, padx=5, pady=5)

        # Campos do formulário
        labels = ['Código:', 'Nome*:', 'Telefone*:', 'Email*:']
        entries = ['codigo_entry', 'nome_entry', 'telefone_entry', 'email_entry']

        for i, (label, entry) in enumerate(zip(labels, entries)):
            Label(self.form_frame, text=label, bg='#f0f0f0').grid(row=i, column=0, sticky=W, padx=5, pady=2)
            setattr(self, entry, Entry(self.form_frame, width=40))
            getattr(self, entry).grid(row=i, column=1, padx=5, pady=2)

        # Botões
        botoes = [
            ('Limpar', self.limpar_campos, '#d9534f'),
            ('Adicionar', self.adicionar_cliente, '#5cb85c'),
            ('Editar', self.editar_cliente, '#f0ad4e'),
            ('Remover', self.remover_cliente, '#d9534f')
        ]

        btn_frame = Frame(self.form_frame, bg='#f0f0f0')
        btn_frame.grid(row=4, columnspan=2, pady=10)

        for text, command, color in botoes:
            Button(btn_frame, text=text, bg=color, fg='white',
                   command=command).pack(side=LEFT, padx=5)

        # Lista de clientes (Treeview)
        self.lista_frame = LabelFrame(self.main_frame, text="Clientes Cadastrados",
                                      bg='#f0f0f0', fg='#333', font=('Arial', 10, 'bold'))
        self.lista_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        colunas = ['Código', 'Nome', 'Telefone', 'Email']
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
        for entry in [self.codigo_entry, self.nome_entry,
                      self.telefone_entry, self.email_entry]:
            entry.delete(0, END)

    def carregar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        clientes = self.serializador.get_models()
        for cliente in clientes:
            self.tree.insert('', END, values=(
                cliente.get('codigo', ''),
                cliente['nome'],
                cliente['telefone'],
                cliente['email']
            ))

    def preencher_campos(self, event):
        self.limpar_campos()
        item = self.tree.selection()[0]
        valores = self.tree.item(item, 'values')

        self.codigo_entry.insert(0, valores[0])
        self.nome_entry.insert(0, valores[1])
        self.telefone_entry.insert(0, valores[2])
        self.email_entry.insert(0, valores[3])

    def validar_campos(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()

        if not nome or not Validadores.validar_nome(nome):
            messagebox.showerror("Erro", "Nome inválido! Deve ter pelo menos 3 caracteres.")
            return False

        if not telefone or not Validadores.validar_telefone(telefone):
            messagebox.showerror("Erro", "Telefone inválido! Formato esperado: (XX)XXXXX-XXXX")
            return False

        if not email or not Validadores.validar_email(email):
            messagebox.showerror("Erro", "Email inválido! Formato esperado: usuario@dominio.com")
            return False

        return True

    def adicionar_cliente(self):
        if not self.validar_campos():
            return

        cliente = Cliente(
            nome=self.nome_entry.get(),
            telefone=self.telefone_entry.get(),
            email=self.email_entry.get()
        )

        self.serializador.adicionar_cliente(cliente)
        self.carregar_clientes()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")

    def editar_cliente(self):
        codigo = self.codigo_entry.get()
        if not codigo:
            messagebox.showerror("Erro", "Selecione um cliente para editar!")
            return

        if not self.validar_campos():
            return

        # Encontra o cliente na lista
        clientes = self.serializador.get_models()
        for i, cliente in enumerate(clientes):
            if str(cliente.get('codigo', '')) == codigo:
                # Atualiza os dados
                clientes[i]['nome'] = self.nome_entry.get()
                clientes[i]['telefone'] = self.telefone_entry.get()
                clientes[i]['email'] = self.email_entry.get()
                break

        self.serializador.save()
        self.carregar_clientes()
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")

    def remover_cliente(self):
        codigo = self.codigo_entry.get()
        if not codigo:
            messagebox.showerror("Erro", "Selecione um cliente para remover!")
            return

        if messagebox.askyesno("Confirmar", "Deseja realmente remover este cliente?"):
            clientes = self.serializador.get_models()
            clientes[:] = [c for c in clientes if str(c.get('codigo', '')) != codigo]
            self.serializador.save()
            self.carregar_clientes()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")


if __name__ == "__main__":
    root = Tk()
    app = PetshopInterface(root)
    root.mainloop()