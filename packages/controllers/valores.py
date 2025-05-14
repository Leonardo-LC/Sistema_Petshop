from packages.controllers.serializador import Serializador
from packages.models.medicovet import MedicoVet
from packages.models.gerente import Gerente
import webbrowser

class Valores:

    def banho(self,peso):
        if peso <= 5:
            return  40
        elif peso <= 10:
            return  50
        elif peso <= 20:
            return  60
        else:
            return  80

    def tosa(self,peso):
        if peso <= 5:
            return 50
        elif peso <= 10:
            return 60
        elif peso <= 20:
            return 70
        else:
            return 90

    def corte_unhas(self,peso):
        if peso <= 10:
            return 20
        elif peso <= 20:
            return 25
        else:
            return 30

    def consulta(self,peso):
        if peso <= 10:
            return 100
        elif peso <= 20:
            return 120
        else:
            return 150

    def chekup(self):
        return 200


