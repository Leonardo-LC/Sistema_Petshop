from packages.controllers.serializador import Serializador
from packages.models.medicovet import MedicoVet
from packages.models.gerente import Gerente
import webbrowser

class Petshop:

    def __init__(self,razao_social):
        self.razao_social = razao_social
        self.clientes = Serializador("")