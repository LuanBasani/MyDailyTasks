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
        CREATE TABLE IF NOT EXISTS prioridade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO prioridade (nome)
        VALUES ('alta'), ('media'), ('baixa')
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas_criadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            prioridade_id INTEGER,
            FOREIGN KEY (prioridade_id) REFERENCES prioridade(id)
        )
    """)

    conn.commit()
    conn.close()

#=====Funçoes=======

def Criar_tarefa():
    #=====cria nova janela do botao===
    nova_janela = tk.Toplevel(janela)
    nova_janela.title("Criar Tarefa")
    nova_janela.geometry("400x300")

    #=====rotulos e entradas=====
    rotulo_nome = tk.Label(nova_janela, text="Nome da Tarefa:")
    rotulo_nome.pack(pady=5)
    entrada_nome = tk.Entry(nova_janela)
    entrada_nome.pack(pady=5)

    rotulo_desc = tk.Label(nova_janela, text="Descriçao: ")
    rotulo_desc.pack(pady=5)
    entrada_desc = tk.Entry(nova_janela)
    entrada_desc.pack(pady=5)

    #=====botoes de selecao da prioridade=====

    valor_prioridade = tk.StringVar()
    valor_prioridade.set("media")
    tk.Radiobutton(nova_janela, text="Alta", variable=valor_prioridade, value="alta").pack()

    tk.Radiobutton(nova_janela, text="Média", variable=valor_prioridade, value="media").pack()
    
    tk.Radiobutton(nova_janela, text="Baixa", variable=valor_prioridade, value="baixa").pack()


    def salvar():
        nome = entrada_nome.get()
        desc = entrada_desc.get()
        prioridade_nome = valor_prioridade.get()
        

        conn = sqlite3.connect("tarefas.db")
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute(
            "SELECT id FROM prioridade WHERE nome = ?",
            (prioridade_nome,)
        )
        prioridade_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO tarefas_criadas (nome, descricao, prioridade_id)
            VALUES (?, ?, ?)
        """, (nome, desc, prioridade_id))

        nova_janela.destroy()
        conn.commit()
        conn.close()

    tk.Button(nova_janela, text="Salvar", command=salvar).pack(pady=10)




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
    tk.Checkbutton(janela, text="oi", variable=valor_check,).pack()

    tk.Checkbutton(janela, text="Saida", variable=valor_check, ).pack()

#====Botao criar tarefa======

   

#====criar a tabela tarefas====
    global tabela
    tabela = ttk.Treeview(janela,columns=(tk.Checkbutton, "nome","descricao","prioridade", tk.Button), show="headings")

    tabela.heading(tk.Checkbutton, text="Feito")
    tabela.heading("nome", text="Nome")
    tabela.heading("descricao", text="Descriçao")
    tabela.heading("prioridade", text="Prioridade")
    tabela.heading(tk.Button,text="Excluir")

    tabela.column(tk.Checkbutton, width=50)
    tabela.column("nome", width=50)
    tabela.column("descricao", width=100)
    tabela.column("prioridade", width=40)
    tabela.column(tk.Button, width=5)

    tabela.pack(padx=10, pady=10, fill="both", expand=True)

    botao_criar = tk.Button(janela, text="Criar nova tarefa", command=Criar_tarefa)
    botao_criar.pack(pady=15)



#====Loop=====
    janela.mainloop()

if __name__ == "__main__":
    criar_banco()
    main()