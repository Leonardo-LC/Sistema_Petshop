import sqlite3

banco = sqlite3.connect('banco.db')

cursor = banco.cursor()

cursor.execute("CREATE TABLE clientes (nome text,telefone text,email text)")

cursor.execute("INSERT INTO clientes VALUES ('Maria', '61981226381', 'mariazinha@gmail.com' )")

banco.commit()
