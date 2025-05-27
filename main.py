from packages.controllers.interface import PetshopInterface
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    app = PetshopInterface(root)
    root.mainloop()