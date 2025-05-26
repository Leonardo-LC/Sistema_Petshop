# 🐾 Sistema Petshop - Gerenciamento Veterinário

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Sistema desktop para gestão completa de petshops, incluindo cadastro de clientes, pets, agendamento de serviços e controle de funcionários. Desenvolvido com foco em praticidade e organização para pequenas clínicas e estabelecimentos veterinários.

---

## 📌 Funcionalidades

### 🧑 Clientes e Pets
- Cadastro de clientes com dados pessoais
- Registro de múltiplos pets por cliente
- Histórico de serviços por animal

### 💼 Funcionários
- Cadastro de médicos veterinários (com CRMV)
- Cadastro de banhistas

### 💰 Serviços
- Cálculo automático de preços (banho, tosa, consultas)
- Tabela de valores baseada no peso do animal
- Registro completo de serviços realizados

---

## 📚 Casos de Uso

### 1. Gerenciamento de Clientes e Pets
- **Cadastrar um novo cliente**: O usuário insere os dados pessoais do cliente, como nome, endereço e telefone.
- **Registrar um pet para um cliente existente**: Após selecionar o cliente, o usuário adiciona informações do pet, como nome, espécie, raça e peso.
- **Consultar histórico de serviços de um pet**: O usuário acessa o perfil do pet para visualizar todos os serviços realizados anteriormente.

### 2. Gerenciamento de Funcionários
- **Adicionar um novo médico veterinário**: Cadastro com nome, especialidade e número do CRMV.
- **Registrar um novo banhista**: Inclusão de dados pessoais de funcionários responsáveis por banho e tosa.

### 3. Agendamento e Realização de Serviços
- **Agendar um serviço para um pet**: Seleção do pet, escolha do serviço (banho, tosa, consulta), definição da data e cálculo automático do preço.
- **Registrar a conclusão de um serviço**: Marcação como "concluído", salvando no histórico do animal.

### 4. Relatórios e Consultas
- **Gerar relatório de serviços por período**: Lista completa dos serviços realizados em determinado intervalo de tempo.
- **Consultar dados de um cliente ou pet específico**: Busca rápida por nome para acesso ao cadastro e histórico.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.10+
- **Interface Gráfica**: Tkinter (GUI)
- **Persistência de dados**: Arquivos JSON

---

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/Leonardo-LC/Sistema_Petshop.git
   cd Sistema_Petshop
2. Instale as dependencias:
   pip install tk

3. Execute o sistema
   python main.py
