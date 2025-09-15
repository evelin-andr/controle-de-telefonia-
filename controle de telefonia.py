import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from turtle import up

class LinhaTelefonica():
    def __init__(self, numero, responsavel, operadora, valor, centro):
       self.numero = numero
       self.responsavel = responsavel
       self.operadora = operadora 
       self.valor = valor
       self.centro = centro 
class ControleTelefonica:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Controle de Telefonia")
        self.dados = []
        self.entries= []
        self.front()

    def front(self):
        # Labels e Entry
        self.label1 = tk.Label(self.janela, text="Linha | Número:")
        self.label1.grid(row=0, column=0)
        self.entry1 = tk.Entry(self.janela)
        self.entry1.grid(row=0, column=1)
        self.entry1.bind("<Return>", lambda event: self.entry2.focus_set())
        self.entries.append(self.entry1)
        
        self.label2 = tk.Label(self.janela, text="Responsável | Usuário:")
        self.label2.grid(row=1, column=0)
        self.entry2 = tk.Entry(self.janela)
        self.entry2.grid(row=1, column=1)
        self.entry2.bind("<Return>", lambda event: self.entry3.focus_set())
        self.entries.append(self.entry2)

        self.label3 = tk.Label(self.janela, text="Operadora:")
        self.label3.grid(row=3, column=0)
        operadoras = ["Vivo", "Claro", "Tim"]
        self.entry3 = ttk.Combobox(self.janela, values=operadoras, width=17)
        self.entry3.grid(row=3, column=1)
        self.entry3.bind("<Return>", lambda event: self.entry4.focus_set())
        self.entries.append(self.entry3)
        

        self.label4 = tk.Label(self.janela, text="Valor da Linha:")
        self.label4.grid(row=4, column=0)
        self.entry4 = tk.Entry(self.janela)
        self.entry4.grid(row=4, column=1)
        self.entry4.bind("<Return>", lambda event: self.entry5.focus_set())
        self.entries.append(self.entry4)
         
        self.label5 = tk.Label(self.janela, text="Centro de custo:")
        self.label5.grid(row=5, column=0)
        self.entry5 = tk.Entry(self.janela)
        self.entry5.grid(row=5, column=1)
        self.entry5.bind("<Return>", lambda event: self.salvar())
        self.entries.append(self.entry5)

        # Botões
        self.button1 = tk.Button(self.janela, text="Salvar", command=self.salvar)
        self.button1.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        
        self.button2 = tk.Button(self.janela, text="Consultar", command=self.consultar)
        self.button2.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        
        self.button3 = tk.Button(self.janela, text="Atualizar", command=self.atualizar)
        self.button3.grid(row=4, column=2, padx=5, pady=5, sticky='w')
        
        # Tabela
        colunas = ("numero", "Responsavel", "Operadora", "Valor", "Centro")
        self.tabela = ttk.Treeview(self.janela, columns=colunas, show="headings")
        self.tabela.heading("numero", text="Linha | Número")
        self.tabela.heading("Responsavel", text="Responsável | Usuário")
        self.tabela.heading("Operadora", text="Operadora")
        self.tabela.heading("Valor", text="Valor da linha")
        self.tabela.heading("Centro", text="Centro de custo")
        self.tabela.grid(row=7, columnspan=3, padx=10, pady=17)
        
        for col in self.tabela["columns"]:
            self.tabela.column(col, width=150, anchor='center') 

        self.entry1.focus_set() #pra sempre começar pelo primeiro campo quando abrir o programa 
        for entry in self.entries:
            entry.bind("<Down>", self.focus_next)
            entry.bind("<Up>", self.focus_prev)

    def focus_next(self, event):
        atual= self.entries.index(event.widget)
        proximo = (atual + 1) % len(self.entries)
        self.entries[proximo].focus_set()          
    def focus_prev(self, event):
        atual = self.entries.index(event.widget)
        anterior = (atual - 1) % len(self.entries)
        self.entries[anterior].focus_set()

    # Métodos 
    def salvar(self):
        numero = self.entry1.get().strip()
        responsavel = self.entry2.get().strip()
        operadora = self.entry3.get().strip()
        valor = self.entry4.get().strip()
        centro = self.entry5.get().strip()

         #verifica se ta tudo preenchido 
        if not numero or not responsavel or not operadora or not valor or not centro:
         messagebox.showerror(title=None, message="Preencha todos os campos!")
         return

        #verifica se tem 11 digitos 
        if len(numero) != 11: 
            messagebox.showerror(title=None, message="Número de telefone inválido, digite um número com 11 digitos!")
            return
        # verifica e altera o valor para float    
        try: 
            valor = float(valor)
        except:
            messagebox.showerror(title=None, message="Valor de linha  inválido, informe um valor numérico!")
            return
        
        #transformar os dados pra ficar bonito na tabela 
        valort = int(valor * 100)/ 100
        valorf = f'R$ {valort:.2f}'.replace(",","x").replace(".",",").replace("x",",")
        centro= centro.upper()
        responsavel = responsavel.title()
        numero = f'( {numero[0:2]}) {numero[2:7]}-{numero[7:11]}'

        #-------------------------------------------------------------------------------
        #adiciona na tabela 
        linha = LinhaTelefonica(numero, responsavel,operadora, valor, centro)
        self.dados.append(linha)
        self.tabela.insert("","end", values=(linha.numero, linha.responsavel, linha.operadora, valorf, linha.centro)) 
        messagebox.showinfo(title=None, message="Linha salva com sucesso!")

        #limpa os campos
        self.limpar()
    def limpar(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry3.set("")
        self.entry4.delete(0, tk.END)
        self.entry5.delete(0, tk.END)

    def consultar(self):
        pass


    def atualizar(self):
        pass
    



if __name__ == '__main__':
    janela = tk.Tk()
    app = ControleTelefonica(janela)
    janela.mainloop()
