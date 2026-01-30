import sqlite3

conn = sqlite3.connect("tarefas.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM tarefas_criadas")
print(cursor.fetchall())

conn.close()