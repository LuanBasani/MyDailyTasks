#====Bibliotecas===

import tkinter as tk
from tkinter import messagebox, ttk

import sqlite3

#======Criando BD=====
def criar_banco():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prioridade(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)
    cursor.execute("INSERT INTO prioridade (nome) VALUES ('alta')")
    cursor.execute("INSERT INTO prioridade (nome) VALUES ('media')")
    cursor.execute("INSERT INTO prioridade (nome) VALUES ('baixa')")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            FOREIGN KEY (prioridade_id) REFERENCES prioridade(id)
        )
    """)
    

    conn.commit()
    conn.close()

#=====Funçoes=======

def Criar_tarefa():
    nova_janela = tk.Toplevel(janela)
    nova_janela.title("Criar Tarefa")
    nova_janela.geometry("400x300")

    tk.Label(nova_janela, text="Nome da Tarefa:").pack(pady=5)
    tk.Entry(nova_janela).pack(pady=5)

    tk.Label(nova_janela, text="Descriçao: ").pack(pady=5)
    tk.Entry(nova_janela).pack(pady=5)

    valor_prioridade = tk.Variable()
    tk.Radiobutton(nova_janela, text="Alta", variable=valor_prioridade, value="alta").pack()

    tk.Radiobutton(nova_janela, text="Média", variable=valor_prioridade, value="media").pack()
    
    tk.Radiobutton(nova_janela, text="Baixa", variable=valor_prioridade, value="baixa").pack()

    tk.Button(nova_janela, text="Salvar").pack(pady=10)

#=====Funçao principal====

def main():

#=====Janela principal====
    global janela
    janela = tk.Tk()
    janela.title("MyDailyTasks")
    janela.geometry("600x700")

    rotulo_titulo = tk.Label(janela,text="MyDailyTasks")
    rotulo_titulo.pack()

#====Check tarefa======
    valor_check = tk.Variable()
    tk.Radiobutton(janela, text="Entrada", variable=valor_check, value="entrada").pack()

    tk.Radiobutton(janela, text="Saida", variable=valor_check, value="saida").pack()

#====Botao criar tarefa======

    botao_criar = tk.Button(janela, text="Criar nova tarefa", command=Criar_tarefa)
    botao_criar.pack(pady=50)

    botao_criar.place(relx=1.0, x=-30, y=100, anchor="ne")

#====Loop=====
    janela.mainloop()

if __name__ == "__main__":
    criar_banco()
    main()