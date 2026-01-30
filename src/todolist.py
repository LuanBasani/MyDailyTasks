#====Bibliotecas===
import tkinter as tk
from tkinter import messagebox, ttk

import sqlite3

#======Criando BD=====
def criar_banco():
    conn = sqlite3.connect("database/tarefas.db")
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
            feito INTEGER,
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
    
    rotulo_prioridade = tk.Label(nova_janela, text="Selecione a prioridade:")
    rotulo_prioridade.pack()

    #=====botoes de selecao da prioridade=====

    valor_prioridade = tk.StringVar()
    valor_prioridade.set("media")
    tk.Radiobutton(nova_janela, text="Alta", variable=valor_prioridade, value="alta").pack()

    tk.Radiobutton(nova_janela, text="Média", variable=valor_prioridade, value="media").pack()
    
    tk.Radiobutton(nova_janela, text="Baixa", variable=valor_prioridade, value="baixa").pack()

    #====Funçao para salvar entradas no banco de dados
    def salvar():
        #=== pegar entradas ===
        nome = entrada_nome.get()
        desc = entrada_desc.get()
        prioridade_nome = valor_prioridade.get()
        
        #====conecta ao banco===
        conn = sqlite3.connect("tarefas.db")
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        #=== verifica o nome com a tabela prioridade e pega id===
        cursor.execute(
            "SELECT id FROM prioridade WHERE nome = ?",
            (prioridade_nome,)
        )
        prioridade_id = cursor.fetchone()[0]

        #==== insere os dados pego ====
        cursor.execute("""
            INSERT INTO tarefas_criadas (nome, descricao, prioridade_id)
            VALUES (?, ?, ?)
        """, (nome, desc, prioridade_id))

        #==== fecha janela, salva e recarrega tabela ====
        nova_janela.destroy()
        conn.commit()
        conn.close()
        carregar_tarefas()

    #=== botao de salvar (puxa funçao) ====
    tk.Button(nova_janela, text="Salvar", command=salvar).pack(pady=10)



#=== funçao para atualizar tabela de acordo com db===
def carregar_tarefas():
    #=== conecta ===
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    #=== cria apelido para tabelas e transforma id em nome da prioridade ===
    cursor.execute("""
        SELECT t.feito, t.nome, t.descricao, p.nome
        FROM tarefas_criadas t
        JOIN prioridade p ON t.prioridade_id = p.id
    """)

    dados = cursor.fetchall()
    conn.close()

    #====limpa a tabela====
    for item in tabela.get_children():
        tabela.delete(item)

    #====insere os dados===
    for feito, nome, desc, prioridade in dados:
        checkbox = "☑" if feito == 1 else "☐"
        tabela.insert("","end",values=(checkbox, nome, desc, prioridade, "Excluir"))



#====Funçao para fazer clique na tabela====
def clique_tabela(event):
    #====reconhece o clique em colunas e linhas====
    item = tabela.identify_row(event.y)
    coluna = tabela.identify_column(event.x)

    #====Reconhecer se o clique foi em uma linha válida====
    if not item:
        return

    #====Transforma cada item das colunas em lista====
    valores = list(tabela.item(item, "values"))

    #====Transformar a coluna 1 em checkbox====
    if coluna == "#1":
    #==== Alternar em marcado ou nao====
        if valores[0] == "☐":
            valores[0] = "☑"
            feito = 1
        else:
            valores[0] = "☐"
            feito = 0

        #====Atualiza a tabela====
        tabela.item(item, values=valores)

        #====Salva no banco de dados====
        conn = sqlite3.connect("tarefas.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tarefas_criadas SET feito = ? WHERE nome = ?",
            (feito, valores[1])
        )
        conn.commit()
        conn.close()

    #====Se cliquer na coluna 5 excluir abre msgbox para confirmaçao de exclusao====
    if coluna == "#5":
        resposta = messagebox.askyesno(
            "Confirmar",
            "Deseja excluir esta tarefa?"
        )
        #====Deleta do banco de dados====
        if resposta:
            conn = sqlite3.connect("tarefas.db")
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tarefas_criadas WHERE nome = ?",
                (valores[1],)
            )
            conn.commit()
            conn.close()
            carregar_tarefas()

#=====Funçao principal====

def main():

    #=====Janela principal====
    global janela
    janela = tk.Tk()
    janela.title("MyDailyTasks")
    janela.geometry("600x700")

    rotulo_titulo = tk.Label(janela,text="MyDailyTasks", font=("Arial", 18, "bold"), fg="#2ab17b",)
    rotulo_titulo.pack()
   

    #====criar a tabela tarefas====
    global tabela
    tabela = ttk.Treeview(janela,columns=("feito", "nome", "descricao", "prioridade", "acoes"), show="headings")

    tabela.heading("feito", text="Feito")
    tabela.heading("nome", text="Nome")
    tabela.heading("descricao", text="Descrição")
    tabela.heading("prioridade", text="Prioridade")
    tabela.heading("acoes", text="Excluir")

    tabela.column("feito", width=50, anchor="center")
    tabela.column("nome", width=120)
    tabela.column("descricao", width=200)
    tabela.column("prioridade", width=80, anchor="center")
    tabela.column("acoes", width=80, anchor="center")

    tabela.pack(padx=10, pady=10, fill="both", expand=False)

    #====Reconhecer clique na tabela====
    tabela.bind("<Button-1>", clique_tabela)

#====Botao criar tarefa======

    botao_criar = tk.Button(janela, text="Criar nova tarefa", bg="#0078d7", fg="white", activebackground="#005a9e", activeforeground="white", command=Criar_tarefa)
    botao_criar.pack(pady=15)

#==== sempre recarrega a tabela qnd abre ====
    carregar_tarefas()



#====Loop=====
    janela.mainloop()

#====Iniciar script====
if __name__ == "__main__":
    criar_banco()
    main()