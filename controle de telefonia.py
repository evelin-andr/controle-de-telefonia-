import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime
import openpyxl
import os



class LinhaTelefonica():
#classe que armazena os dados da linha 
    def __init__(self, numero, responsavel, operadora, valor, centro, status, data_cadastro):
       self.numero = numero
       self.responsavel = responsavel
       self.operadora = operadora 
       self.valor = valor
       self.centro = centro 
       self.status = status
       self.data_cadastro = data_cadastro
class ControleTelefonica:
    
    def __init__(self, janela):
        self.janela = janela 
        self.janela.title("Controle de Telefonia")  
        self.janela.configure(bg="lightgreen")

        #diretório para exportação da planilha
        self.entries= []
        DB_DIR = "C:\\Exportacoes"
        DB_FILE = os.path.join(DB_DIR, "banco_telefonia.db")
        
        try:
            os.makedirs(DB_DIR, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Erro de Diretório", f"Não foi possível criar o diretório: {DB_DIR}\nErro: {e}")
            self.janela.destroy() 
            return

        #conexão com o banco de dados
        self.banco = sqlite3.connect(DB_FILE)
        self.cursor = self.banco.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS dados (linha TEXT, responsavel TEXT, operadora TEXT, valor REAL, centro_c TEXT, status INTEGER, data_cadastro TEXT)") 
        self.modo_atualizar = False
        self.linha_em_edicao = None
        self.front()
       
    def check_numero_limite(self, texto):
        #só aceita se for número no telefone e tiver no máximo 11 dígitos
        if texto == "":
            return True
        if texto.isdigit() and len(texto) <= 11:
            return True
        else:
            return False

    def check_apenas_texto(self, texto):
        # Permite  apenas texto em centro de custo e que não contenha dígitos
        if texto == "":
            return True
        return not any(char.isdigit() for char in texto)

        

    def front(self):
       
        # Labels e Entry
        vld_numero = (self.janela.register(self.check_numero_limite), '%P')
        self.label1 = tk.Label(self.janela, text="Linha | Número:")
        self.label1.grid(row=1, column=0)
        self.label1.configure(bg="lightgreen")

        self.entry1 = tk.Entry(self.janela, validate="key", validatecommand=vld_numero)
        self.entry1.grid(row=1, column=1)
        self.entry1.bind("<Return>", lambda event: self.entry2.focus_set())
        self.entries.append(self.entry1)
        
        self.label2 = tk.Label(self.janela, text="Responsável | Usuário:")
        self.label2.grid(row=2, column=0)
        self.label2.configure(bg="lightgreen")

        self.entry2 = tk.Entry(self.janela)
        self.entry2.grid(row=2, column=1)
        self.entry2.bind("<Return>", lambda event: self.entry3.focus_set())
        self.entries.append(self.entry2)

        self.label3 = tk.Label(self.janela, text="Operadora:")
        self.label3.grid(row=3, column=0)
        self.label3.configure(bg="lightgreen")

        operadoras = ["Vivo", "Claro", "Tim"]
        self.entry3 = ttk.Combobox(self.janela, values=operadoras, width=17)
        self.entry3.grid(row=3, column=1)
        self.entry3.bind("<Return>", lambda event: self.entry4.focus_set())
        self.entries.append(self.entry3)
        

        self.label4 = tk.Label(self.janela, text="Valor da Linha:")
        self.label4.grid(row=4, column=0)
        self.label4.configure(bg="lightgreen")

        self.entry4 = tk.Entry(self.janela)
        self.entry4.grid(row=4, column=1)
        self.entry4.bind("<Return>", lambda event: self.entry5.focus_set())
        self.entries.append(self.entry4)
         
        self.label5 = tk.Label(self.janela, text="Setor de custo:")
        self.label5.grid(row=5, column=0)
        self.label5.configure(bg="lightgreen")

        vcmd = (self.janela.register(self.check_apenas_texto), '%P')

        self.entry5 = tk.Entry(self.janela, validate="key", validatecommand=vcmd)
        self.entry5.grid(row=5, column=1)
        self.entry5.bind("<Return>", lambda event: self.salvar())
        self.entries.append(self.entry5)

        # Botões
        self.button1 = tk.Button(self.janela, text="💾 Salvar", command=self.salvar, bd=3, )
        self.button1.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.button1.bind("<Return>", lambda event: self.entry1.focus_set())

        self.button2 = tk.Button(self.janela, text="🔍 Consultar", command=self.consultar, bd=3)
        self.button2.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        
        self.button3 = tk.Button(self.janela, text="🔄 Atualizar", command=self.atualizar,bd=3)
        self.button3.grid(row=3, column=2, padx=5, pady=5, sticky='w')
        self.button4 = tk.Button(self.janela, text="❌ Inativar", command=self.excluir, bd=3)
        self.button4.grid(row=4, column=2, padx=5, pady=5, sticky='w')

        self.button5 = tk.Button(self.janela, text="📤 Exportar", command=self.exportar, bd=3)
        self.button5.grid(row=5 , column=2, padx=5, pady=5, sticky='w')
        
        
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

        #pra sempre começar pelo primeiro campo quando abrir o programa 
        self.entry1.focus_set() 
        for entry in self.entries:
            entry.bind("<Down>", self.focus_next)
            entry.bind("<Up>", self.focus_prev)

    #navegação entre os campos com as setas 
    def focus_next(self, event):
        atual= self.entries.index(event.widget)
        proximo = (atual + 1) % len(self.entries)
        self.entries[proximo].focus_set()       

    def focus_prev(self, event):
        atual = self.entries.index(event.widget)
        anterior = (atual - 1) % len(self.entries)
        self.entries[anterior].focus_set()  

    def salvar(self):
        numero = self.entry1.get().strip()
        responsavel = self.entry2.get().strip()
        operadora = self.entry3.get().strip()
        valor = self.entry4.get().strip()
        centro = self.entry5.get().strip()
        status = 1
        data_cadastro = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

        #verificação de campos vazios
        if not numero or not responsavel or not operadora or not valor or not centro:
         messagebox.showerror(title=None, message="Preencha todos os campos!")
         return

        if len(numero) != 11: 
            messagebox.showerror(title=None, message="Número de telefone inválido, digite um número com 11 digitos!")
            return  
        try: 
            valor = float(valor)
        except:
            messagebox.showerror(title=None, message="Valor de linha  inválido, informe um valor numérico!")
            return

        #uso do salvar para o atualizar
        if self.modo_atualizar:
            confirmar = messagebox.askyesno("Confirmar atualização",f"Tem certeza que deseja atualizar a linha {self.linha_em_edicao}?")
            if not confirmar:
                return

            self.cursor.execute("UPDATE dados SET responsavel=?, operadora=?, valor=?, centro_c=? WHERE linha=?",(responsavel.title(), operadora, valor, centro.upper(), self.linha_em_edicao))
            self.banco.commit()

            messagebox.showinfo("Sucesso", "Linha atualizada com sucesso!")
            self.modo_atualizar = False
            self.linha_em_edicao = None
            self.consultar()
            self.limpar()


        else:  
        #usa o salvar pra salvar no banco  
        #transformar os dados pra ficar bonito na tabela 
            centro= centro.upper()
            responsavel = responsavel.title()
            numero = f'({numero[0:2]}){numero[2:7]}-{numero[7:11]}'
            valor = f"R$ {valor:.2f}"
            # verifica duplicidade 
            try:
                self.cursor.execute("SELECT 1 FROM dados WHERE linha = ? LIMIT 1", (numero,))
                if self.cursor.fetchone():
                    messagebox.showerror(title=None, message="Já existe uma linha com esse número cadastrada.")
                    return
            except sqlite3.Error as e:
                messagebox.showerror("Erro no Banco de Dados", f"Falha ao verificar duplicidade: {e}")
                return
    
            #-------------------------------------------------------------------------------
            #adiciona na tabela 
            
            linha = LinhaTelefonica(numero, responsavel,operadora, valor, centro, status, data_cadastro)
            self.tabela.insert("","end", values=(linha.numero, linha.responsavel, linha.operadora, linha.valor, linha.centro, linha.status, linha.data_cadastro)) 
            #adiciona no banco 
            self.cursor.execute("INSERT INTO dados VALUES(?, ?, ?, ?, ?, ?,?)", (linha.numero, linha.responsavel, linha.operadora, linha.valor, linha.centro, linha.status, linha.data_cadastro))
            self.banco.commit()
            
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
        # limpa tabela antes da consulta
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        self.consulta_linha = self.entry1.get().strip()
        self.consulta_nome = self.entry2.get().strip()

        if self.consulta_linha == "" and self.consulta_nome == "":
            messagebox.showwarning(title=None, message="Nenhum dado para consulta! Informe a linha ou o responsável.")
            return

        if len(self.consulta_linha) != 11 and len(self.consulta_linha) != 0: 
            messagebox.showerror(title=None, message="Número de telefone inválido, digite um número com 11 digitos!")
            return

        #consulta pelo número de telefone
        if self.consulta_linha != "":
            self.consulta_linha = f'({self.consulta_linha[0:2]}){self.consulta_linha[2:7]}-{self.consulta_linha[7:11]}'
     
        
            self.cursor.execute("SELECT linha, responsavel, operadora, valor, centro_c FROM dados WHERE status = 1 AND linha = ?",(self.consulta_linha,))
            resultados = self.cursor.fetchall()
            
            if not resultados:
                self.cursor.execute("SELECT linha, responsavel, operadora, valor, centro_c, status FROM dados WHERE status = 0 AND linha = ?",(self.consulta_linha,))
                inativa = self.cursor.fetchall()
                if not resultados:
                        messagebox.showinfo(title= "Erro",message=f"Não foi encontrado nenhum registro referente a '{self.consulta_linha}' no banco de dados")
        
                if inativa:
                    resposta = messagebox.askyesno("Linha inativada",f"A linha {self.consulta_linha} está inativada. Deseja visualizar o histórico dessa linha?")

                    if resposta:
                        resultados = inativa 
        #consulta pelo nome
        elif self.consulta_nome:

            self.cursor.execute("SELECT linha, responsavel, operadora, valor, centro_c FROM dados WHERE status = 1 AND responsavel LIKE ?",(f"%{self.consulta_nome}%",))
            resultados = self.cursor.fetchall()
            
            if not resultados:
                self.cursor.execute("SELECT linha, responsavel, operadora, valor, centro_c FROM dados WHERE status = 0 AND responsavel LIKE ?",(f"%{self.consulta_nome}%",))
                inativas = self.cursor.fetchall()

                if inativas:
                    if messagebox.askyesno( "Registros inativados",f"Encontramos linhas inativadas para '{self.consulta_nome}'. Deseja visualizar?"):
                        resultados = inativas
                if not resultados:
                    messagebox.showinfo(title= "Erro",message=f"Não foi encontrado nenhum registro referente a '{self.consulta_nome}' no banco de dados")
            
        # exibe na tabela
        for linha in resultados:  
            self.tabela.insert("", "end", values=linha)
      
    def fechar(self):
        self.banco.close()

    def atualizar(self):
        selecionados = self.tabela.selection()
        if not selecionados:
            messagebox.showerror("Erro", "Selecione uma linha para atualizar.")
            return

        self.linha_selecionada = selecionados[0]
        valores = self.tabela.item(self.linha_selecionada, 'values')
        numero_linha = valores[0]

        # Verifica se a linha está ativa no banco antes de preencher os campos
        try:
            self.cursor.execute("SELECT status FROM dados WHERE linha = ?", (numero_linha,))
            result_status = self.cursor.fetchone()
        except sqlite3.Error:
            messagebox.showerror("Erro", "Falha ao consultar o status da linha no banco de dados.")
            return

        if result_status and result_status[0] == 0:
            messagebox.showinfo(title=None, message="Não é possível atualizar uma linha inativada.")
            return
        # joga valores nos Entry
        self.entry1.delete(0, tk.END)
        self.entry1.insert(0, numero_linha.replace("(", "").replace(")","").replace("-",""))

        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, valores[1])

        self.entry3.set(valores[2])
        self.entry4.delete(0, tk.END)

        self.entry4.insert(0, valores[3])
        self.entry5.delete(0, tk.END)

        self.entry5.insert(0, valores[4])

        # ativa modo edição
        self.modo_atualizar = True
        self.linha_em_edicao = numero_linha

    def excluir(self):
     selecionados = self.tabela.selection()
     if not selecionados:
        messagebox.showerror("Erro", "Por favor, selecione uma linha para inativar.")
        return
     linha_selecionada = selecionados[0]
    
     valores = self.tabela.item(linha_selecionada, 'values')
     numero_linha = valores[0] 

     confirmar = messagebox.askyesno("Confirmar Inativação",f"Tem certeza que deseja inativar a linha {numero_linha}?")

     if confirmar:
        try:
            self.cursor.execute("UPDATE dados SET status = 0 WHERE linha = ?", (numero_linha,))
            self.banco.commit()
            
            messagebox.showinfo("Sucesso", f"A linha {numero_linha} foi inativada com sucesso!")
            self.tabela.delete(linha_selecionada)
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao inativar a linha: {e}")

    def exportar(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

      
        janela_export = tk.Toplevel(self.janela)
        janela_export.title("Exportar Dados")
        janela_export.geometry("400x250")
        janela_export.resizable(False, False)

        tk.Label(janela_export, text="Filtrar por operadora").pack(pady=5)
        self.operadora_exportar = tk.StringVar(value= "Todas")
        operadoras = ["Todas", "Vivo", "Claro", "Tim"]

        filtro_operadora = tk.Frame(janela_export)
        filtro_operadora.pack(pady=5)

        for linha in operadoras: tk.Radiobutton(filtro_operadora, text=linha, variable=self.operadora_exportar, value=linha).pack(side="left", padx=5)
        
        tk.Label(janela_export, text="Filtrar por status:").pack(pady=5)

        self.status_exportar = tk.StringVar(value="Ativas")
        status_op = ["Ativas", "Inativas", "Todas"]

        filtro_status = tk.Frame(janela_export)
        filtro_status.pack(pady=5)
        

        for st in status_op: tk.Radiobutton(filtro_status, text=st, variable= self.status_exportar, value=st ).pack(side="left", padx=5)

     # --- Botões (Exportar / Cancelar) ---
        frame_botoes = tk.Frame(janela_export)
        frame_botoes.pack(pady=20)
        
        
        btn_exportar = tk.Button(frame_botoes, text="Exportar", command=lambda: self.exportar_dados( self.operadora_exportar.get(), self.status_exportar.get() ), width=12 )
        btn_exportar.pack(side="left", padx=10)
        
        btn_cancelar = tk.Button(frame_botoes, text="Cancelar", command=janela_export.destroy, width=12)
        btn_cancelar.pack(side="left", padx=10)
  
    def exportar_dados(self, operadora_filtro, status_filtro):
     # Monta consulta conforme filtros
     consulta = "SELECT linha, responsavel, operadora, valor, centro_c, status, data_cadastro FROM dados WHERE 1=1"
     params = []
 
     if operadora_filtro != "Todas":
         consulta += " AND operadora = ?"
         params.append(operadora_filtro)
 
     if status_filtro == "Ativas":
         consulta += " AND status = 1"

     elif status_filtro == "Inativas":
         consulta += " AND status = 0"
 
     self.cursor.execute(consulta, params)
     resultados = self.cursor.fetchall()
 
     if not resultados:
         messagebox.showinfo("Sem dados", "Nenhum dado encontrado com esses filtros.")
         return
 
     # Cria a planilha
     criar_planilha = openpyxl.Workbook()
     cp = criar_planilha.active
     cp.title = "Linhas Telefônicas"
 
     # Cabeçalho
     cabecalho = ["Linha", "Responsável", "Operadora", "Valor", "Centro de Custo", "Status", "Data de Cadastro"]
     cp.append(cabecalho)
 
     for linha in resultados:
         linha = list(linha)
         linha[5] = "Ativa" if linha[5] == 1 else "Inativa"  # Converte status
         cp.append(linha)
 
     pasta_export = "C:\\Exportacoes"
     try:
         os.makedirs(pasta_export, exist_ok=True)
     except Exception as e:
         messagebox.showerror("Erro de Diretório", f"Não foi possível criar o diretório de exportação: {pasta_export}\nErro: {e}")
         return

     data_atual = datetime.datetime.now().strftime('%d-%m-%Y')
     nome_base = "Numeros_Comerciais"
     
     
     if operadora_filtro != "Todas":
         nome_base += f"_{operadora_filtro}"
     
    
     if status_filtro != "Todas":
         nome_base += f"_{status_filtro}"
     
 
     nome_arquivo = f"{nome_base}_{data_atual}.xlsx"
     
     # Define o caminho completo do arquivo
     caminho_completo = os.path.join(pasta_export, nome_arquivo)
     
     # Salva a planilha no diretório ProgramData
     criar_planilha.save(caminho_completo)
 
     messagebox.showinfo("Exportação concluída", f"Planilha exportada como:\n{caminho_completo}")


     self.fechar()
   
if __name__ == '__main__':
    janela = tk.Tk()
    app = ControleTelefonica(janela)
    janela.mainloop()
