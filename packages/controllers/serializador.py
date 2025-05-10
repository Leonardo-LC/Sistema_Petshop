import json

class Serializador:

    def __init__(self, arquivo):
        self.__arquivo = "packages/controllers/database/" + arquivo
        self.__models = []
        self.read()

    def save(self):
        try:
            with open(self.__arquivo, "w") as fjson:
                json.dump(self.__models, fjson, indent=4, ensure_ascii=False)
        except Exception as erro:
            print(f'Erro durante o salvamento dos dados: {erro}')


    def read(self):
        try:
            with open(self.__arquivo, "r") as fjson:
                self.__models = json.load(fjson)
        except FileNotFoundError:
            print(f'Arquivo inexistente')
            self.__models = []

    def __write(self, model):
        try:
            self.__models.append(model.to_dict())
            self.save()
        except Exception as erro:
            print(f'Erro ao adicionar {erro}')

    def __erase(self, model):
        try:
            self.__models.remove(model.to_dict())
            self.save()
        except Exception as erro:
            print(f'Não foi possível remover: {erro}')

    def get_models(self):
        return self.__models

    def verify_number(self,telefone):
        for model in self.__models:
            if telefone == model["telefone"]:
                return True
        return False


#Parte que cuida da adição e subtração no banco de dados

    def contratar(self,model):
        self.__write(model)

    def demitir(self,model):
        self.__erase(model)

    def adicionar_cliente(self,model):
        self.__write(model)

    def remover_cliente(self,model):
        self.__erase(model)

