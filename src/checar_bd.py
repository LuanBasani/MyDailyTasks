import sqlite3

conn = sqlite3.connect("tarefas.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM prioridade")
print(cursor.fetchall())

conn.close()