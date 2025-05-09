from packages.controllers.petshop import Petshop

def workspace():

    app = Petshop('PetTop')
    app.menu()

if __name__ == "__main__":
    workspace()