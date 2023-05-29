#Interação com utilizador
import tkinter as tk
from model.listaLigada import*
from model.utilizador import*
from tkinter import messagebox
import re
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from model.manipuladorarquivos import*



class View:
    def __init__(self,master):
        self.master=master
        self.lista_utilizador = listaLigada()
        self.carrega_lista_utilizador = ManipulaArquivos()
        self.lista_utilizador = self.carrega_lista_utilizador.ler_ficheiro_json()
        
        #Frame
        self.master.resizable(False, False)
        self.frame = tk.Frame(self.master,width=20000, height=20000, bg='#808080',padx=100,pady=100)
        self.frame.pack()
    

        #Imagem
        self.logo = tk.PhotoImage(file='OIG.n6q73a.-removebg-preview.png')
        self.logo = self.logo.subsample(2)
        self.logo_label = tk.Label(self.frame, image=self.logo, bg='#808080')
        self.logo_label.place(relx=1.0, anchor='ne')
        self.logo_label.pack() 

        self.label_titulo = tk.Label(self.frame,text="SCDM: Sistemas de Controlo de Despesas Mensais",font=('Corbel Light', 16), bg='#808080')
        self.label_titulo.pack()

        #Label + Entry para username
        self.nome_label = tk.Label(self.frame, text="Nome", font=('Corbel Light', 16), bg='#808080')
        self.nome_label.pack()
        self.nome_entry = tk.Entry(self.frame, font=('Arial', 16))
        self.nome_entry.pack(pady=5)

        #Label + Entry para password
        self.password_label = tk.Label(self.frame, text="Password", font=('Corbel Light', 16), bg='#808080')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.frame, show="*", font=('Arial', 16),bg='#F0F8FF')
        self.password_entry.pack(pady=5)
        
        #Botao da senha
        self.mostra_password_botao= tk.Button(self.frame,text="Mostrar senha", font=('Arial',8),fg='white',bg='#4F4F4F',command=self.vizualicao_password)
        self.mostra_password_botao.pack()

        #Botões de Login + registo
        self.login_button = tk.Button(self.frame, text="Login", font=('InK Free',20),fg='black', bg='#00BFFF', command=self.logar_utilizador)
        self.login_button.pack(pady=10, ipadx=20, ipady=5)
        self.registo_button = tk.Button(self.frame, text="Registo", font=('InK Free',20), fg='white', bg='#0000CD',command=self.registrar_utlizador)
        self.registo_button.pack(pady=10, ipadx=20, ipady=5)
        
        


     ################################################################################################
     # O metodo logar deve ser chamado se o utilizador estiver registrado já 
    
    def registrar_utlizador(self):
        ##############################################################################################
        #Frame para o registro
        self.janela_registro = tk.Toplevel(self.master,padx=200,pady=100,bg='#808080')
        self.janela_registro.resizable(False,False)
        self.registro_label = tk.Label(self.janela_registro,bg='#808080')
        self.registro_label.pack()
   
        #################################################################################################
        #Label + Entry para username
        self.nome_label2 = tk.Label(self.registro_label, text="Digite o seu nome de usuário", font=('Corbel Light', 16),bg='#808080')
        self.nome_label2.pack()
        self.nome_entry2 = tk.Entry(self.registro_label, font=('Arial', 16))
        self.nome_entry2.pack(pady=5)

        #################################################################################################
        #Label + Entry para NIF
        self.nif_label = tk.Label(self.registro_label,text="Digite o seu Nif", font=('Corbel Light', 16),bg='#808080')
        self.nif_label.pack()
        self.nif_entry = tk.Entry(self.registro_label, font=('Arial', 16))
        self.nif_entry.pack(pady=5)

        ###################################################################################################
        #Label + Entry para password
        self.password_label2 = tk.Label(self.registro_label,text="Digite uma senha", font=('Corbel Light', 16),bg='#808080')
        self.password_label2.pack()
        self.password_entry2 = tk.Entry(self.registro_label, show="*", font=('Arial', 16),bg='#F0F8FF')
        self.password_entry2.pack(pady=5)

        ####################################################################################################
        # Botão vizualisa senha
        #Botao da senha
        self.mostra_password_registo_botao = tk.Button(self.registro_label,text="Mostrar senha", font=('Arial',8),fg='white',bg='#4F4F4F',command=self.vizualiza_password_registro)
        self.mostra_password_registo_botao.pack()

        #####################################################################################################
        #Label + Entry para confirmacao da password
        self.confirma_password_label = tk.Label(self.registro_label,text="Confirma a sua senha", font=('Corbel Light', 16),bg='#808080') 
        self.confirma_password_label.pack()
        self.confirma_password_entry = tk.Entry(self.registro_label, show="*", font=('Arial', 16),bg='#F0F8FF')
        self.confirma_password_entry.pack(pady=5)

        ########################################################################################################
        # Botão vizualisa senha
        self.mostra_confirma_password_registo_botao2 = tk.Button(self.registro_label,text="Mostrar senha", font=('Arial',8),fg='white',bg='#4F4F4F',command=self.vizualisa_confirmacao_senha)
        self.mostra_confirma_password_registo_botao2.pack()

        #botão para finalizar registro
        self.botao_finaliza_registro = tk.Button(self.registro_label, text="Registrar", font=('InK Free', 12), bg='#00BFFF',command=self.finalizar_registro_utilizador)
        self.botao_finaliza_registro.pack(ipady=2)

        
        
    def finalizar_registro_utilizador(self):
        nome_usuario = self.nome_entry2.get()
        nif = self.nif_entry.get()
        senha = self.password_entry2.get()
        confirmancao_senha = self.confirma_password_entry.get()

        if nome_usuario=='' or nif=='' or senha=='' or confirmancao_senha=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return 

        if not nif.isdigit() or len(nif) != 9:
            messagebox.showerror('Erro no NIF', 'O NIF deve conter 9 números') 
            return   

        if senha != confirmancao_senha:
          messagebox.showerror('Senha', 'Confirmação da senha incorreta')   
          return            
        
        pos=self.lista_utilizador.find_username(nome_usuario)
        
        usuario=self.lista_utilizador.get(pos)
        

        if usuario is None: 
           no_atual = self.lista_utilizador.head
           nif_verifica = int(nif)

           while no_atual is not None:# Verifica se o nif já existe
               if no_atual.element.get_nif() == nif_verifica: 
                   messagebox.showerror('Atenção','Este nif já foi associado a outro utilizador')
                   return 
               no_atual = no_atual.next_node
         
           self.cliente = Utilizador(nome_usuario, int(nif), senha)
           self.lista_utilizador.insert_last(self.cliente)
           self.carrega_lista_utilizador.salvar_dados_em_json(self.lista_utilizador)
           messagebox.showinfo('Registro', 'Registrado com sucesso')

        else:
            messagebox.showerror('Registro','Este utilizador já foi registrado')

 
    #################################################################################################
    # Os metodos abaixo do metodo logar_utilizador só podem chamados depois do utilizador estar logado
    
    def logar_utilizador(self):
        if self.nome_entry.get() and self.password_entry.get():
             
             nome = self.nome_entry.get()
             
             pos=self.lista_utilizador.find_username(nome)
             
             utilizador=self.lista_utilizador.get(pos)
             
             if utilizador is not None and self.password_entry.get()==utilizador.get_password():
                  messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                  # Abrir as opções 
                  self.janela_login = tk.Toplevel(self.master,padx=200,pady=100,bg='#808080')
                  self.janela_login.resizable(False,False)
                  self.janela_label = tk.Label(self.janela_login,bg='#808080')
                  self.janela_label.pack()

                  self.botao_define_orcamento = tk.Button(self.janela_label,text="Definir orçamento",font=('InK Free', 16),bg='#00BFFF', command=self.definir_orcamento)
                  self.botao_define_orcamento.pack()

                  self.botao_registrar_despesa = tk.Button(self.janela_label,text="Adicinar despesa",font=('InK Free', 16), bg='#00BFFF',command = self.registrar_despesa)
                  self.botao_registrar_despesa.pack()

                  self.botao_visualizar_despesas = tk.Button(self.janela_label,text="Visualizar despesas",font=('InK Free', 16),bg='#00BFFF', command = self.vizualizar_despesas)
                  self.botao_visualizar_despesas.pack()

                  self.botao_sugerir_cortes = tk.Button(self.janela_label,text="Sugestão de cortes",font=('InK Free', 16), bg='#00BFFF',command = self.sugerir_cortes)
                  self.botao_sugerir_cortes.pack()

             else:
                  messagebox.showerror("Erro", "Nome de usuário ou senha incorretos!")
        else:
             messagebox.showerror("Erro", "Preencha todos os campos!") 


    ###############################################################################################################
    
    
    def registrar_despesa(self):
       
        self.registro_despesa_janela = tk.Toplevel(self.master,padx=200,pady=100,bg='#808080') 
        self.registro_despesa_janela.resizable(False,False)
        self.tela_registro_despesa =  tk.Label(self.registro_despesa_janela,bg='#808080')
        self.tela_registro_despesa.pack()

        # DATA Label e Entry
        self.label_data = tk.Label(self.tela_registro_despesa,text="Digite a data(DD/MM/AAAA). Ex: 18/11/2000", font=('Corbel Light', 16),bg='#808080')
        self.label_data.pack()
        self.entry_data = tk.Entry(self.tela_registro_despesa,font=('Arial', 16))
        self.entry_data.pack()

        # Categoria Label e Entry
        self.label_categoria = tk.Label(self.tela_registro_despesa,text="Categoria da despesa",font=('Corbel Light', 16),bg='#808080') 
        self.label_categoria.pack()
        self.entry_categoria = tk.Entry(self.tela_registro_despesa,font=('Arial', 16))
        self.entry_categoria.pack()

        # Valor Label e Entry
        self.label_valor = tk.Label(self.tela_registro_despesa,text="Valor gasto para despesa(EUR)",font=('Corbel Light', 16),bg='#808080')
        self.label_valor.pack()
        self.entry_valor = tk.Entry(self.tela_registro_despesa,font=('Arial', 16))
        self.entry_valor.pack()

        # Descrição dacdespesa Label e Entry
        self.label_descDespesa = tk.Label(self.tela_registro_despesa,text="Descrição da despesa",font=('Corbel Light', 16),bg='#808080')
        self.label_descDespesa.pack()
        self.entry_desDespesa = tk.Entry(self.tela_registro_despesa,font=('Arial', 16))
        self.entry_desDespesa.pack()
        
        # Botão para finalizar registro de despesa 
        self.adiciona_despesa_registrada = tk.Button(self.tela_registro_despesa,text="Adicionar despesa",font=('InK Free', 12), bg='#00BFFF',command = self.finalizar_registro_despesa)
        self.adiciona_despesa_registrada.pack()

    def finalizar_registro_despesa(self):

        data_despesa = self.entry_data.get()
        categoria_despesa =  self.entry_categoria.get()
        valor_despesa = self.entry_valor.get()
        descDespesa = self.entry_desDespesa.get()
        padrao = r"\d{2}/\d{2}/\d{4}"
        
        if re.match(padrao,data_despesa):
            self.cliente.adicionar_despesa(data_despesa,categoria_despesa,float(valor_despesa),descDespesa) 
            self.carrega_lista_utilizador.salvar_dados_em_json(self.lista_utilizador)
        else: 
            messagebox.showwarning('Registro despesa','A data da despesa deve estar no formato DD/MM/AA')   

        
    #####################################################################################################################    


    def vizualizar_despesas(self):
        self.visualiza_despesa_janela = tk.Toplevel(self.master,padx=200,pady=100,bg='#808080')
        self.visualiza_despesa_janela.resizable(True,True)
        self.tela_visualiza_despesas = tk.Label(self.visualiza_despesa_janela,bg='#808080')
        self.tela_visualiza_despesas.pack()

        # botão para visualizar as despesas em formato de tabela
        self.botao_visualiza_despesas_tabela = tk.Button(self.tela_visualiza_despesas,text="Mostrar despesas em tabela",font=('InK Free', 16), bg='#00BFFF',command = self.tabela_despesas)
        self.botao_visualiza_despesas_tabela.pack()

        # botão para visualizar as despesas em formato de gráfico
        self.botao_visualiza_despesas_grafico = tk.Button(self.tela_visualiza_despesas,text="Mostrar despesas em formato de gráfico",font=('InK Free', 16), bg='#00BFFF',command = self.grafico_despesas)
        self.botao_visualiza_despesas_grafico.pack()

        self.botao_escolha_tempo_despesa = tk.Button(self.tela_visualiza_despesas,text="Escolha o periodo de tempo para o qual deseja visualizar as suas despesas",font=('InK Free', 16), bg='#00BFFF',command = self.visualiza_despesas_periodo_tempo)
        self.botao_escolha_tempo_despesa.pack()

        self.botao_visualiza_despesas_ordenadas = tk.Button(self.tela_visualiza_despesas,text="Visualizar as despesas ordenadas por valor",font=('InK Free', 16), bg='#00BFFF',command = self.visualiza_despesas_ordenadas)
        self.botao_visualiza_despesas_ordenadas.pack()

        self.botao_visualiza_despesas_categoria = tk.Button(self.tela_visualiza_despesas,text="Filtrar gastos por categoria",font=('InK Free', 16), bg='#00BFFF',command = self.visualiza_despesas_categoria)
        self.botao_visualiza_despesas_categoria.pack()

    def visualiza_despesas_categoria(self): 
        lista_filtrada = self.cliente.filtrar_listaDespesa()
        self.despesas_filtradas_janela = tk.Toplevel(self.master,padx=60,pady=60,bg='#808080')
        self.despesas_filtradas_janela.resizable(True,False) 
        self.despesas_filtradas_tela = tk.Label(self.despesas_filtradas_janela)
        self.despesas_filtradas_tela.pack()
        info_despesas = ""
        no_atual = lista_filtrada.head
        label_titulo = tk.Label(self.despesas_filtradas_tela,text="Lista de despesas filtrada por categoria",font=('Arial Black', 16))
        label_titulo.pack()
        while no_atual is not None:
            info_despesas +=f"Categoria: {no_atual.element.get_categoria()} ->Valor: {no_atual.element.get_valor()}\n" 
            no_atual = no_atual.next_node
        label_info_despesas = tk.Label(self.despesas_filtradas_tela,text=info_despesas,font=('Arial', 16)) 
        label_info_despesas.pack()    
    

    def visualiza_despesas_ordenadas(self):
        self.cliente.Ordena_listaDespesas()  
        self.despesas_ordenadas_janela = tk.Toplevel(self.master,padx=60,pady=60,bg='#808080')
        self.despesas_ordenadas_janela.resizable(True,False)
        self.despesas_ordenadas_tela = tk.Label(self.despesas_ordenadas_janela) 
        self.despesas_ordenadas_tela.pack()

        no_atual = self.cliente.get_listaDespesas().head
        info_despesa = ""
        label_titulo = tk.Label(self.despesas_ordenadas_tela,text="Lista de despesas ordenadas por valor",font=('Arial Black', 16))
        label_titulo.pack()

        while no_atual is not None:
            info_despesa +=f"Descrição: {no_atual.element.get_descricaoDespesa()} -> valor: {no_atual.element.get_valor()} -> Categoria: {no_atual.element.get_categoria()} -> Data: {no_atual.element.get_data()}\n"

            no_atual = no_atual.next_node
        
        label_info_despesas = tk.Label(self.despesas_ordenadas_tela,text=info_despesa,font=('Arial', 16)) 
        label_info_despesas.pack()   

    



    def visualiza_despesas_periodo_tempo(self):

        self.despesas_periodo_tempo_janela = tk.Toplevel(self.master,padx=60,pady=60,bg='#808080')
        self.despesas_periodo_tempo_janela.resizable(False,False)
        self.despesas_periodo_tmpo_tela = tk.Label(self.despesas_periodo_tempo_janela) 
        self.despesas_periodo_tmpo_tela.pack()   

        # Label + Entry data inicio
        self.label_data_inicio = tk.Label(self.despesas_periodo_tmpo_tela,text="Insira a data de inicio no formato (DD/MM/AAAA)",font=('Corbel Light', 16))
        self.label_data_inicio.pack()
        self.entry_data_inicio = tk.Entry(self.despesas_periodo_tmpo_tela,font=('Arial', 16))
        self.entry_data_inicio.pack()

        # Label + Entry data final
        self.label_data_final = tk.Label(self.despesas_periodo_tmpo_tela,text="Insira a data final no formato (DD/MM/AAAA)",font=('Corbel Light', 16))
        self.label_data_final.pack()
        self.entry_data_final = tk.Entry(self.despesas_periodo_tmpo_tela,font=('Arial', 16))
        self.entry_data_final.pack()


        #botao para ir visualizar as despesas num periodo de tempo
        self.botao_visualizacao_filtragem = tk.Button(self.despesas_periodo_tmpo_tela,text="Ver a filtragem",font=('InK Free', 16), bg='#00BFFF',command = self.finaliza_visualiza_despesas_periodo_tempo)
        self.botao_visualizacao_filtragem.pack()


    def finaliza_visualiza_despesas_periodo_tempo(self):
        
        self.fa_va_despesas_periodo_tempo_janela = tk.Toplevel(self.master,padx=60,pady=60,bg='#808080') 
        self.fa_va_despesas_periodo_tempo_janela.resizable(False,False)
        self.fa_va_despesas_p_tmp_tela = tk.Label(self.fa_va_despesas_periodo_tempo_janela)
        self.fa_va_despesas_p_tmp_tela.pack()


        data_inicio = self.entry_data_inicio.get()
        data_final = self.entry_data_final.get() 

        data_inicio = datetime.strptime(data_inicio,"%d/%m/%Y")
        data_final = datetime.strptime(data_final,"%d/%m/%Y")

        
        if data_inicio >= data_final:
            messagebox.showerror('Alerta','O periodo de tempo inserido não é compatível')
            return

        
        lista_despesa_filtrada = self.cliente.filtra_listaDespesas_periodo(data_inicio,data_final)   
        no_atual = lista_despesa_filtrada.head
        info_despesas = ""

            
        while no_atual is not None:
            info_despesas += f"Descrição: {no_atual.element.get_descricaoDespesa()} -> valor: {no_atual.element.get_valor()} -> Categoria: {no_atual.element.get_categoria()} -> Data: {no_atual.element.get_data()}\n"
            no_atual = no_atual.next_node  

        label_titulo = tk.Label(self.fa_va_despesas_p_tmp_tela,text="filtragem das despesas por periodo",font=('Arial Black', 16))
        label_titulo.pack()

        label_info_despesas = tk.Label(self.fa_va_despesas_p_tmp_tela,text=info_despesas,font=('Arial', 14))
        label_info_despesas.pack()
    


                
    def tabela_despesas(self):
        self.tabela_janela = tk.Toplevel(self.master,padx=200,pady=100,bg='#808080')
        self.tabela_janela.resizable(True,False)
        self.tabela_tela = tk.Label(self.tabela_janela,bg='#00BFFF')
        self.tabela_tela.pack()

        label_titulo = tk.Label(self.tabela_tela,text="Gráfico da lista de despesas",font=('Arial Black', 16),bg='#00BFFF')
        label_titulo.pack()


        self.table_label = tk.Label(self.tabela_tela, text="", justify=tk.CENTER,font=('Arial', 16),bg='#00BFFF')
        self.table_label.pack()

        df = self.cliente.consulta_listaDespesa_tabela()
        tabela_string = df.to_string(index=False)

        self.table_label.config(text=tabela_string)

    def grafico_despesas(self):
        figura = self.cliente.consulta_listaDespesas_grafico()

        # Criar um objeto FigureCanvasTkAgg com a figura
        canvas = FigureCanvasTkAgg(figura,master=self.tela_visualiza_despesas)
        canvas.draw()

        # Exibir o widget de tela do gráfico
        canvas.get_tk_widget().pack()
  

    #####################################################################################################################


    def definir_orcamento(self):
        self.orcamento_tela = tk.Toplevel(self.master,padx=50,pady=50,bg='#808080')
        self.orcamento_tela.resizable(False,False)
        self.janela_orcamento = tk.Label(self.orcamento_tela,bg='#808080')
        self.janela_orcamento.pack()

        # Orçamento Label e Entry
        self.orcamento_label = tk.Label(self.janela_orcamento,text="Defina o orçamneto mensal(EUR)", font=('Corbel Light', 16),bg='#808080')
        self.orcamento_label.pack()
        self.orcamento_entry = tk.Entry(self.janela_orcamento,font=('Arial', 16)) 
        self.orcamento_entry.pack()

        # Botão para finalizar 
        self.botao_finaliza_orcamento = tk.Button(self.janela_orcamento,text="Definir orçamento ",font=('InK Free', 16), bg='#00BFFF',command = self.finaliza_definir_orcamento)
        self.botao_finaliza_orcamento.pack()

    def finaliza_definir_orcamento(self):  
        orcamento = self.orcamento_entry.get()
        self.cliente.set_orcamento(float(orcamento))
        self.carrega_lista_utilizador.salvar_dados_em_json(self.lista_utilizador)
        messagebox.showinfo('Orçamento','Orçamento definido com sucesso')



#########################################################################################################################

    def sugerir_cortes(self):

        if isinstance(self.cliente.analisa_historico_despesas(),Despesas):
            despesa = self.cliente.analisa_historico_despesas()

            self.sugerir_tela = tk.Toplevel(self.master,padx=50,pady=50,bg='#808080')
            self.sugerir_tela.resizable(False,False)
            self.janela_sugerir_cortes = tk.Label(self.sugerir_tela,bg='#808080')
            self.janela_sugerir_cortes.pack()

            label_titulo = tk.Label(self.janela_sugerir_cortes,text="Sugestões de cortes",font=('Arial Black', 16),bg='#808080')
            label_titulo.pack()

            orcamento = f"\nOrçamento mensal: {self.cliente.get_orcamento()} EUR"

            label_orcamento = tk.Label(self.janela_sugerir_cortes,text=orcamento,font=('Arial', 14),bg='#808080')
            label_orcamento.pack()

            info_despesa = f"\nCategoria: {despesa.get_categoria()}, Media dos gastos da categoria: {despesa.get_valor()}"

            label_sugestao = tk.Label(self.janela_sugerir_cortes,text="\nSugere-se o corte da seguinte categoria que é a que mais gastou",font=('Arial', 14,'underline'),bg='#808080')
            label_sugestao.pack()

            label_despesa = tk.Label(self.janela_sugerir_cortes,text=info_despesa,font=('Arial', 14),bg='#808080')
            label_despesa.pack()

            
        
        elif isinstance(self.cliente.analisa_historico_despesas(),listaLigada):
            lista_historico_despesa = self.cliente.analisa_historico_despesas()
            
            self.sugerir_tela = tk.Toplevel(self.master,padx=50,pady=50,bg='#808080')
            self.sugerir_tela.resizable(False,False)
            self.janela_sugerir_cortes = tk.Label(self.sugerir_tela,bg='#808080')
            self.janela_sugerir_cortes.pack()

            label_titulo = tk.Label(self.janela_sugerir_cortes,text="Sugestões de cortes",font=('Arial Black', 16),bg='#808080')
            label_titulo.pack()

            orcamento = f"\nOrçamento mensal: {self.cliente.get_orcamento()} EUR"

            label_orcamento = tk.Label(self.janela_sugerir_cortes,text=orcamento,font=('Arial', 14),bg='#808080')
            label_orcamento.pack()

            no_atual = lista_historico_despesa.head

            info_despesas = ""

            while no_atual is not None:
                info_despesas += f"Categoria: {no_atual.element.get_categoria()}, Valor médio gasto na categoria{no_atual.element.get_valor()}"
                no_atual = no_atual.next_node

            label_sugestao = tk.Label(self.janela_sugerir_cortes,text="\nSugere-se o corte das seguintes categorias que são as que mais gastou",font=('Arial', 14,'underline'),bg='#808080')
            label_sugestao.pack()

            label_despesa = tk.Label(self.janela_sugerir_cortes,text=info_despesas,font=('Arial', 14),bg='#808080')
            label_despesa.pack()
    

        else:
           messagebox.showinfo('Despesa','Não foi inserida nenhuma despesa')
                 


###################################################################################################################

    def vizualicao_password(self):
        if self.password_entry.cget("show")=="*":
            self.password_entry.configure(show="")
            self.mostra_password_botao.configure(text="Ocultar Senha")
        else:
            self.password_entry.configure(show="*")
            self.mostra_password_botao.configure(text="Mostrar Senha")  

###################################################################################################################


    def vizualiza_password_registro(self):  
        if self.password_entry2.cget("show")=="*":
            self.password_entry2.configure(show="")
            self.mostra_password_registo_botao.configure(text="Ocultar Senha")
        else:
            self.password_entry2.configure(show="*")    
            self.mostra_password_registo_botao.configure(text="Mostrar Senha")
###################################################################################################################            

    def vizualisa_confirmacao_senha(self):  
        if self.confirma_password_entry.cget("show")=="*":
            self.confirma_password_entry.configure(show="")
            self.mostra_confirma_password_registo_botao2.configure(text="Ocultar Senha")
        else:
            self.confirma_password_entry.configure(show="*")
            self.mostra_confirma_password_registo_botao2.configure(text="Mostrar Senha")

                  
            
                   

    