from tkinter import *
from tkinter import ttk, messagebox
from packages.controllers.serializador import Serializador
from packages.models.cliente import Cliente
from packages.models.animal import Animal
from packages.models.medicovet import MedicoVet
from packages.models.banhista import Banhista
from packages.controllers.validadores import Validadores
from packages.controllers.valores import Valores
from datetime import datetime
import re


class PetshopInterface:
    def __init__(self, root):
        self.root = root
        self.valores = Valores()
        self.style = ttk.Style()
        self.configurar_estilos()
        self.configurar_janela()
        self.criar_widgets()
        self.serializador_clientes = Serializador("database_clientes.json")
        self.serializador_medicos = Serializador("database_medicos.json")
        self.serializador_banhistas = Serializador("database_banhistas.json")
        self.carregar_clientes()
        self.carregar_medicos()
        self.carregar_banhistas()

    def configurar_estilos(self):
        self.style.theme_use('clam')
        self.style.configure('.', background='#f5f5f5', foreground='#333333')
        self.style.configure('TNotebook', background='#f5f5f5', borderwidth=0)
        self.style.configure('TNotebook.Tab', background='#e1e1e1', padding=[10, 5], font=('Helvetica', 10, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', '#4a90e2')], foreground=[('selected', 'white')])
        self.style.configure('TButton', font=('Helvetica', 10), padding=6)
        self.style.map('TButton',
                       foreground=[('active', 'white'), ('!disabled', 'white')],
                       background=[('active', '#3a7bc8'), ('!disabled', '#4a90e2')])
        self.style.configure('Treeview', font=('Helvetica', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'), background='#e1e1e1')
        self.style.map('Treeview', background=[('selected', '#4a90e2')], foreground=[('selected', 'white')])
        self.style.configure('TLabel', font=('Helvetica', 10))
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5)

    def configurar_janela(self):
        self.root.title("🐾 Sistema Petshop 🐾")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f5f5f5')
        self.root.resizable(True, True)

        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        position_right = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - window_height / 2)
        self.root.geometry(f"+{position_right}+{position_down}")

    def criar_widgets(self):
        self.notebook = ttk.Notebook(self.root, style='TNotebook')
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.aba_clientes = Frame(self.notebook, bg='#f5f5f5')
        self.aba_medicos = Frame(self.notebook, bg='#f5f5f5')
        self.aba_banhistas = Frame(self.notebook, bg='#f5f5f5')

        self.notebook.add(self.aba_clientes, text="🐶 Clientes e Pets")
        self.notebook.add(self.aba_medicos, text="🏥 Médicos Veterinários")
        self.notebook.add(self.aba_banhistas, text="🛁 Banhistas")

        self.criar_aba_clientes()
        self.criar_aba_medicos()
        self.criar_aba_banhistas()

    def criar_aba_clientes(self):
        self.form_frame_cliente = LabelFrame(
            self.aba_clientes,
            text="📝 Cadastro de Clientes e Pets",
            bg='#f5f5f5', fg='#333333',
            font=('Helvetica', 11, 'bold'),
            padx=10, pady=10,
            relief=FLAT
        )
        self.form_frame_cliente.pack(fill=X, padx=15, pady=(5, 10))

        frame_cliente = Frame(self.form_frame_cliente, bg='#f5f5f5')
        frame_cliente.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        frame_pet = Frame(self.form_frame_cliente, bg='#f5f5f5')
        frame_pet.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        labels_cliente = ['Nome*:', 'Telefone*:', 'Email*:']
        entries_cliente = ['nome_entry', 'telefone_entry', 'email_entry']

        for i, (label, entry) in enumerate(zip(labels_cliente, entries_cliente)):
            lbl = Label(frame_cliente, text=label, bg='#f5f5f5', font=('Helvetica', 10))
            lbl.grid(row=i, column=0, sticky=W, padx=5, pady=5)
            ent = Entry(frame_cliente, width=30, font=('Helvetica', 10),
                        relief=SOLID, borderwidth=1)
            ent.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, entry, ent)

        labels_pet = ['Nome Pet*:', 'Idade*:', 'Peso (kg)*:', 'Tipo*(cachorro, gato, coelho ou hamster):', 'Serviços(banho, tosa, cortar unhas, consulta):']
        entries_pet = ['nome_pet_entry', 'idade_entry', 'peso_entry', 'tipo_entry', 'servicos_entry']

        for i, (label, entry) in enumerate(zip(labels_pet, entries_pet)):
            lbl = Label(frame_pet, text=label, bg='#f5f5f5', font=('Helvetica', 10))
            lbl.grid(row=i, column=0, sticky=W, padx=5, pady=5)
            ent = Entry(frame_pet, width=30, font=('Helvetica', 10),
                        relief=SOLID, borderwidth=1)
            ent.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, entry, ent)

        btn_frame = Frame(self.form_frame_cliente, bg='#f5f5f5')
        btn_frame.grid(row=1, columnspan=2, pady=(10, 0))

        botoes = [
            ('🧹 Limpar', self.limpar_campos, '#e74c3c'),
            ('➕ Adicionar', self.adicionar_cliente_pet, '#2ecc71'),
            ('🗑️ Remover', self.remover_cliente, '#e74c3c')
        ]

        for text, command, color in botoes:
            btn = Button(
                btn_frame, text=text, command=command,
                bg=color, fg='white', font=('Helvetica', 10, 'bold'),
                activebackground=color, activeforeground='white',
                relief=FLAT, padx=10, pady=5, bd=0
            )
            btn.pack(side=LEFT, padx=5)
            if color == '#e74c3c':
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#c0392b'))
                btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

        self.lista_frame_cliente = LabelFrame(
            self.aba_clientes,
            text="📋 Clientes e Pets Cadastrados",
            bg='#f5f5f5', fg='#333333',
            font=('Helvetica', 11, 'bold'),
            padx=10, pady=10,
            relief=FLAT
        )
        self.lista_frame_cliente.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))

        colunas = ['Nome', 'Telefone', 'Email', 'Pet', 'Tipo', 'Idade', 'Peso', 'Serviços', 'Total']
        self.tree_cliente = ttk.Treeview(
            self.lista_frame_cliente,
            columns=colunas,
            show='headings',
            style='Treeview'
        )

        for col in colunas:
            self.tree_cliente.heading(col, text=col)
            self.tree_cliente.column(col, width=100, anchor=CENTER)

        self.tree_cliente.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.tree_cliente.bind('<Double-1>', self.preencher_campos)

        scroll = ttk.Scrollbar(
            self.tree_cliente,
            orient="vertical",
            command=self.tree_cliente.yview
        )
        scroll.pack(side=RIGHT, fill=Y)
        self.tree_cliente.configure(yscrollcommand=scroll.set)

    def criar_aba_medicos(self):
        self.form_frame_medico = LabelFrame(
            self.aba_medicos,
            text="📝 Cadastro de Médicos Veterinários",
            bg='#f5f5f5', fg='#333333',
            font=('Helvetica', 11, 'bold'),
            padx=10, pady=10,
            relief=FLAT
        )
        self.form_frame_medico.pack(fill=X, padx=15, pady=(5, 10))

        labels = [
            'Nome*:', 'Email*:', 'Telefone*:',
            'Salário*:', 'Data Admissão*:', 'CRMV*:'
        ]
        entries = [
            'medico_nome_entry', 'medico_email_entry', 'medico_telefone_entry',
            'medico_salario_entry', 'medico_data_entry', 'medico_crmv_entry'
        ]

        for i, (label, entry) in enumerate(zip(labels, entries)):
            row = i // 2
            col = i % 2 * 2
            lbl = Label(
                self.form_frame_medico,
                text=label,
                bg='#f5f5f5',
                font=('Helvetica', 10)
            )
            lbl.grid(row=row, column=col, sticky=W, padx=5, pady=5)

            ent = Entry(
                self.form_frame_medico,
                width=30,
                font=('Helvetica', 10),
                relief=SOLID,
                borderwidth=1
            )
            ent.grid(row=row, column=col + 1, padx=5, pady=5)
            setattr(self, entry, ent)

        btn_frame = Frame(self.form_frame_medico, bg='#f5f5f5')
        btn_frame.grid(row=3, columnspan=4, pady=(10, 0))

        botoes = [
            ('🧹 Limpar', self.limpar_campos_medico, '#e74c3c'),
            ('➕ Adicionar', self.adicionar_medico, '#2ecc71'),
            ('🗑️ Remover', self.remover_medico, '#e74c3c')
        ]

        for text, command, color in botoes:
            btn = Button(
                btn_frame, text=text, command=command,
                bg=color, fg='white', font=('Helvetica', 10, 'bold'),
                activebackground=color, activeforeground='white',
                relief=FLAT, padx=10, pady=5, bd=0
            )
            btn.pack(side=LEFT, padx=5)
            if color == '#e74c3c':
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#c0392b'))
                btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

        self.lista_frame_medico = LabelFrame(
            self.aba_medicos,
            text="📋 Médicos Cadastrados",
            bg='#f5f5f5', fg='#333333',
            font=('Helvetica', 11, 'bold'),
            padx=10, pady=10,
            relief=FLAT
        )
        self.lista_frame_medico.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))

        colunas = ['Nome', 'Email', 'Telefone', 'Salário', 'Admissão', 'CRMV']
        self.tree_medico = ttk.Treeview(
            self.lista_frame_medico,
            columns=colunas,
            show='headings',
            style='Treeview'
        )

        for col in colunas:
            self.tree_medico.heading(col, text=col)
            self.tree_medico.column(col, width=120, anchor=CENTER)

        self.tree_medico.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.tree_medico.bind('<Double-1>', self.preencher_campos_medico)

        scroll = ttk.Scrollbar(
            self.tree_medico,
            orient="vertical",
            command=self.tree_medico.yview
        )
        scroll.pack(side=RIGHT, fill=Y)
        self.tree_medico.configure(yscrollcommand=scroll.set)

    def criar_aba_banhistas(self):
        self.form_frame_banhista = LabelFrame(
            self.aba_banhistas,
            text="📝 Cadastro de Banhistas",
            bg='#f5f5f5', fg='#333333',
            font=('Helvetica', 11, 'bold'),
            padx=10, pady=10,
            relief=FLAT
        )
        self.form_frame_banhista.pack(fill=X, padx=15, pady=(5, 10))

        labels = [
            'Nome*:', 'Email*:', 'Telefone*:',
            'Salário*:', 'Data Admissão*:'
        ]
        entries = [
            'banhista_nome_entry', 'banhista_email_entry', 'banhista_telefone_entry',
            'banhista_salario_entry', 'banhista_data_entry'
        ]

        for i, (label, entry) in enumerate(zip(labels, entries)):
            row = i // 2
            col = i % 2 * 2
            lbl = Label(
                self.form_frame_banhista,
                text=label,
                bg='#f5f5f5',
                font=('Helvetica', 10)
            )
            lbl.grid(row=row, column=col, sticky=W, padx=5, pady=5)

            ent = Entry(
                self.form_frame_banhista,
                width=30,
                font=('Helvetica', 10),
                relief=SOLID,
                borderwidth=1
            )
            ent.grid(row=row, column=col + 1, padx=5, pady=5)
            setattr(self, entry, ent)

        btn_frame = Frame(self.form_frame_banhista, bg='#f5f5f5')
        btn_frame.grid(row=3, columnspan=4, pady=(10, 0))

        botoes = [
            ('🧹 Limpar', self.limpar_campos_banhista, '#e74c3c'),
            ('➕ Adicionar', self.adicionar_banhista, '#2ecc71'),
            ('🗑️ Remover', self.remover_banhista, '#e74c3c')
        ]

        for text, command, color in botoes:
            btn = Button(
                btn_frame, text=text, command=command,
                bg=color, fg='white', font=('Helvetica', 10, 'bold'),
                activebackground=color, activeforeground='white',
                relief=FLAT, padx=10, pady=5, bd=0
            )
            btn.pack(side=LEFT, padx=5)
            if color == '#e74c3c':
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#c0392b'))
                btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

        self.lista_frame_banhista = LabelFrame(
            self.aba_banhistas,
            text="📋 Banhistas Cadastrados",
            bg='#f5f5f5', fg='#333333',
            font=('Helvetica', 11, 'bold'),
            padx=10, pady=10,
            relief=FLAT
        )
        self.lista_frame_banhista.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))

        colunas = ['Nome', 'Email', 'Telefone', 'Salário', 'Admissão']
        self.tree_banhista = ttk.Treeview(
            self.lista_frame_banhista,
            columns=colunas,
            show='headings',
            style='Treeview'
        )

        for col in colunas:
            self.tree_banhista.heading(col, text=col)
            self.tree_banhista.column(col, width=120, anchor=CENTER)

        self.tree_banhista.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.tree_banhista.bind('<Double-1>', self.preencher_campos_banhista)

        scroll = ttk.Scrollbar(
            self.tree_banhista,
            orient="vertical",
            command=self.tree_banhista.yview
        )
        scroll.pack(side=RIGHT, fill=Y)
        self.tree_banhista.configure(yscrollcommand=scroll.set)

    # Métodos para Clientes
    def limpar_campos(self):
        for entry in [self.nome_entry, self.telefone_entry, self.email_entry,
                      self.nome_pet_entry, self.idade_entry, self.peso_entry,
                      self.tipo_entry, self.servicos_entry]:
            entry.delete(0, END)

    def carregar_clientes(self):
        for item in self.tree_cliente.get_children():
            self.tree_cliente.delete(item)

        clientes = self.serializador_clientes.get_models()
        for cliente in clientes:
            if cliente['pets']:
                for pet in cliente['pets']:
                    total = sum(pet['servicos_contratados'].values()) if pet['servicos_contratados'] else 0
                    servicos = ", ".join(pet['servicos_contratados'].keys()) if pet['servicos_contratados'] else ""

                    self.tree_cliente.insert('', END, values=(
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
                self.tree_cliente.insert('', END, values=(
                    cliente['nome'],
                    cliente['telefone'],
                    cliente['email'],
                    "", "", "", "", "", ""
                ))

    def preencher_campos(self, event):
        self.limpar_campos()
        item = self.tree_cliente.selection()[0]
        valores = self.tree_cliente.item(item, 'values')

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

        clientes = self.serializador_clientes.get_models()
        cliente_existente = next((c for c in clientes if c['telefone'] == self.telefone_entry.get()), None)

        if cliente_existente:
            cliente_existente['nome'] = self.nome_entry.get()
            cliente_existente['email'] = self.email_entry.get()

            nome_pet = self.nome_pet_entry.get()
            if nome_pet:
                try:
                    idade = int(self.idade_entry.get())
                    peso = float(self.peso_entry.get())
                    tipo = self.tipo_entry.get()
                    servicos = [s.strip().lower() for s in self.servicos_entry.get().split(',') if s.strip()]

                    novo_pet = {
                        'nome': nome_pet,
                        'idade': idade,
                        'peso': peso,
                        'tipo': tipo,
                        'dono_nome': cliente_existente['nome'],
                        'servicos_contratados': {}
                    }

                    for servico in servicos:
                        valor = self.valores.valor_servico(servico, peso)
                        if valor > 0:
                            novo_pet['servicos_contratados'][servico] = valor
                        else:
                            messagebox.showwarning("Aviso", f"Serviço '{servico}' não reconhecido e será ignorado")

                    cliente_existente['pets'].append(novo_pet)

                except ValueError:
                    messagebox.showerror("Erro", "Idade e Peso devem ser números válidos!")
                    return

            self.serializador_clientes.save()

        else:
            cliente = {
                'nome': self.nome_entry.get(),
                'telefone': self.telefone_entry.get(),
                'email': self.email_entry.get(),
                'pets': []
            }

            nome_pet = self.nome_pet_entry.get()
            if nome_pet:
                try:
                    idade = int(self.idade_entry.get())
                    peso = float(self.peso_entry.get())
                    tipo = self.tipo_entry.get()
                    servicos = [s.strip().lower() for s in self.servicos_entry.get().split(',') if s.strip()]

                    novo_pet = {
                        'nome': nome_pet,
                        'idade': idade,
                        'peso': peso,
                        'tipo': tipo,
                        'dono_nome': cliente['nome'],
                        'servicos_contratados': {}
                    }

                    for servico in servicos:
                        valor = self.valores.valor_servico(servico, peso)
                        if valor > 0:
                            novo_pet['servicos_contratados'][servico] = valor
                        else:
                            messagebox.showwarning("Aviso", f"Serviço '{servico}' não reconhecido e será ignorado")

                    cliente['pets'].append(novo_pet)

                except ValueError:
                    messagebox.showerror("Erro", "Idade e Peso devem ser números válidos!")
                    return

            self.serializador_clientes.get_models().append(cliente)
            self.serializador_clientes.save()

        self.carregar_clientes()
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

    def remover_cliente(self):
        item_selecionado = self.tree_cliente.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione um cliente para remover!")
            return

        valores = self.tree_cliente.item(item_selecionado[0], 'values')

        if messagebox.askyesno("Confirmar", "Deseja realmente remover este cliente e seus pets?"):
            clientes = self.serializador_clientes.get_models()
            clientes[:] = [c for c in clientes if c['telefone'] != valores[1]]
            self.serializador_clientes.save()
            self.carregar_clientes()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")

    # Métodos para Médicos
    def limpar_campos_medico(self):
        for entry in [self.medico_nome_entry, self.medico_email_entry, self.medico_telefone_entry,
                      self.medico_salario_entry, self.medico_data_entry, self.medico_crmv_entry]:
            entry.delete(0, END)

    def carregar_medicos(self):
        for item in self.tree_medico.get_children():
            self.tree_medico.delete(item)

        medicos = self.serializador_medicos.get_models()
        for medico in medicos:
            self.tree_medico.insert('', END, values=(
                medico['nome'],
                medico['email'],
                medico['telefone'],
                f"R$ {medico['salario']:.2f}",
                medico['data_admissao'],
                medico['CRMV']
            ))

    def preencher_campos_medico(self, event):
        self.limpar_campos_medico()
        item = self.tree_medico.selection()[0]
        valores = self.tree_medico.item(item, 'values')

        self.medico_nome_entry.insert(0, valores[0])
        self.medico_email_entry.insert(0, valores[1])
        self.medico_telefone_entry.insert(0, valores[2])
        self.medico_salario_entry.insert(0, valores[3].replace("R$ ", ""))
        self.medico_data_entry.insert(0, valores[4])
        self.medico_crmv_entry.insert(0, valores[5])

    def validar_campos_medico(self):
        nome = self.medico_nome_entry.get()
        email = self.medico_email_entry.get()
        telefone = self.medico_telefone_entry.get()
        salario = self.medico_salario_entry.get()
        data = self.medico_data_entry.get()
        crmv = self.medico_crmv_entry.get()

        if not nome or not Validadores.validar_nome(self, nome):
            messagebox.showerror("Erro", "Nome inválido! Deve ter pelo menos 3 caracteres.")
            return False

        if not email or not Validadores.validar_email(self, email):
            messagebox.showerror("Erro", "Email inválido! Formato esperado: usuario@dominio.com")
            return False

        if not telefone or not Validadores.validar_telefone(self, telefone):
            messagebox.showerror("Erro", "Telefone inválido! Formato esperado: (XX)XXXXX-XXXX")
            return False

        try:
            float(salario)
        except ValueError:
            messagebox.showerror("Erro", "Salário deve ser um número válido!")
            return False

        try:
            datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA")
            return False

        if not crmv:
            messagebox.showerror("Erro", "CRMV é obrigatório!")
            return False

        return True

    def adicionar_medico(self):
        if not self.validar_campos_medico():
            return

        try:
            medicos = self.serializador_medicos.get_models()
            medico_existente = next((m for m in medicos if m['CRMV'] == self.medico_crmv_entry.get()), None)

            if medico_existente:
                messagebox.showerror("Erro", "Médico com este CRMV já cadastrado!")
                return

            medico = {
                'nome': self.medico_nome_entry.get(),
                'email': self.medico_email_entry.get(),
                'telefone': self.medico_telefone_entry.get(),
                'salario': float(self.medico_salario_entry.get()),
                'data_admissao': self.medico_data_entry.get(),
                'CRMV': self.medico_crmv_entry.get()
            }

            self.serializador_medicos.get_models().append(medico)
            self.serializador_medicos.save()
            self.carregar_medicos()
            self.limpar_campos_medico()
            messagebox.showinfo("Sucesso", "Médico cadastrado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def remover_medico(self):
        item_selecionado = self.tree_medico.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione um médico para remover!")
            return

        valores = self.tree_medico.item(item_selecionado[0], 'values')

        if messagebox.askyesno("Confirmar", "Deseja realmente remover este médico?"):
            medicos = self.serializador_medicos.get_models()
            medicos[:] = [m for m in medicos if m['CRMV'] != valores[5]]
            self.serializador_medicos.save()
            self.carregar_medicos()
            self.limpar_campos_medico()
            messagebox.showinfo("Sucesso", "Médico removido com sucesso!")


    def limpar_campos_banhista(self):
        for entry in [self.banhista_nome_entry, self.banhista_email_entry, self.banhista_telefone_entry,
                      self.banhista_salario_entry, self.banhista_data_entry]:
            entry.delete(0, END)

    def carregar_banhistas(self):
        for item in self.tree_banhista.get_children():
            self.tree_banhista.delete(item)

        banhistas = self.serializador_banhistas.get_models()
        for banhista in banhistas:
            self.tree_banhista.insert('', END, values=(
                banhista['nome'],
                banhista['email'],
                banhista['telefone'],
                f"R$ {banhista['salario']:.2f}",
                banhista['data_admissao']
            ))

    def preencher_campos_banhista(self, event):
        self.limpar_campos_banhista()
        item = self.tree_banhista.selection()[0]
        valores = self.tree_banhista.item(item, 'values')

        self.banhista_nome_entry.insert(0, valores[0])
        self.banhista_email_entry.insert(0, valores[1])
        self.banhista_telefone_entry.insert(0, valores[2])
        self.banhista_salario_entry.insert(0, valores[3].replace("R$ ", ""))
        self.banhista_data_entry.insert(0, valores[4])

    def validar_campos_banhista(self):
        nome = self.banhista_nome_entry.get()
        email = self.banhista_email_entry.get()
        telefone = self.banhista_telefone_entry.get()
        salario = self.banhista_salario_entry.get()
        data = self.banhista_data_entry.get()

        if not nome or not Validadores.validar_nome(self, nome):
            messagebox.showerror("Erro", "Nome inválido! Deve ter pelo menos 3 caracteres.")
            return False

        if not email or not Validadores.validar_email(self, email):
            messagebox.showerror("Erro", "Email inválido! Formato esperado: usuario@dominio.com")
            return False

        if not telefone or not Validadores.validar_telefone(self, telefone):
            messagebox.showerror("Erro", "Telefone inválido! Formato esperado: (XX)XXXXX-XXXX")
            return False

        try:
            float(salario)
        except ValueError:
            messagebox.showerror("Erro", "Salário deve ser um número válido!")
            return False

        try:
            datetime.strptime(data, '%d/%m/%Y')
        except ValueError:
            messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA")
            return False

        return True

    def adicionar_banhista(self):
        if not self.validar_campos_banhista():
            return

        try:
            banhistas = self.serializador_banhistas.get_models()
            banhista_existente = next((b for b in banhistas if b['telefone'] == self.banhista_telefone_entry.get()),
                                      None)

            if banhista_existente:
                messagebox.showerror("Erro", "Banhista com este telefone já cadastrado!")
                return

            banhista = {
                'nome': self.banhista_nome_entry.get(),
                'email': self.banhista_email_entry.get(),
                'telefone': self.banhista_telefone_entry.get(),
                'salario': float(self.banhista_salario_entry.get()),
                'data_admissao': self.banhista_data_entry.get()
            }

            self.serializador_banhistas.get_models().append(banhista)
            self.serializador_banhistas.save()
            self.carregar_banhistas()
            self.limpar_campos_banhista()
            messagebox.showinfo("Sucesso", "Banhista cadastrado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def remover_banhista(self):
        item_selecionado = self.tree_banhista.selection()
        if not item_selecionado:
            messagebox.showerror("Erro", "Selecione um banhista para remover!")
            return

        valores = self.tree_banhista.item(item_selecionado[0], 'values')

        if messagebox.askyesno("Confirmar", "Deseja realmente remover este banhista?"):
            banhistas = self.serializador_banhistas.get_models()
            banhistas[:] = [b for b in banhistas if b['telefone'] != valores[2]]
            self.serializador_banhistas.save()
            self.carregar_banhistas()
            self.limpar_campos_banhista()
            messagebox.showinfo("Sucesso", "Banhista removido com sucesso!")

            


