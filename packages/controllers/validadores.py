import re

class Validadores:


    def validar_email(self, email: str) -> bool:
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(padrao, email) is not None


    def validar_telefone(self, telefone: str) -> bool:
        padrao = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
        return re.match(padrao, telefone) is not None


    def validar_nome(self, nome: str) -> bool:
        padrao = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+$'
        return re.match(padrao, nome) is not None and len(nome.strip()) >= 3