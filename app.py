import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def validar_login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    if usuario == "medico" and senha =="123"
        print()


app = ctk.CTk()
app.geometry("800x700")
app.title("Sistema de login")

texto_usuario = ctk.CTkLabel(app,text='Usuário')
texto_usuario.pack(pady=10)
campo_usuario = ctk.CTkEntry(app,placeholder_text='Digite seu usuário')
campo_usuario.pack(pady=10)

texto_senha = ctk.CTkLabel(app,text='Senha')
texto_senha.pack(pady=10)
campo_senha = ctk.CTkEntry(app,placeholder_text='Digite sua senha')
campo_senha.pack(pady=10)

button = ctk.CTkButton(app,text='Login',command=validar_login)
button.pack(pady=10)



app.mainloop()
