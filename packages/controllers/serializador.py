import json

class Serializador:

    def __init__(self, arquivo):
        self.__arquivo = "packages/controllers/database" + arquivo
        self.__models = []
        self.read()

    def save(self):
        try:
            with open(self.__arquivo, "w") as fjson:
                json.dump(self.__models, fjson, ident=4, ensure_ascii=False)
        except Exception as erro:
            print(f'Erro durante o salvamento dos dados: {erro}')


    def read(self):
        try:
            with open(self.__arquivo, "r") as fjson:
                self.__models = json.load(fjson)
        except FileExistsError:
            print(f'Arquivo inexistente')
            self.__models = []

    def __write(self, model):
        try:
            self.__models.append(vars(model))
            self.save()
        except Exception as erro:
            print(f'Erro ao adicionar {erro}')

    #def __erase(self,model)    #Trabalhar lógica de apagar funcionário

    def get_models(self):
        return self.__models

