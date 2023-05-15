from despesas import*
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from listaLigada import*
from datetime import datetime
from tkinter import messagebox

class Utilizador:
    
    def __init__(self,nome: str,nif: int,password: str):
        self.__nome:str = nome
        self.__nif:int = nif
        self.__password:str = password        
        self.__listaDespesas = listaLigada() # Lista ligada
        self.__orcamento: float = None 

#################################################################################################################################
# Metodos getters e setters
    def set_orcamento(self,orcamento):
        self.__orcamento = orcamento # Definição do orçamento

    def get_orcamento(self):
        return self.__orcamento    

    def set_nome(self,nome):
        self.__nome=nome
  
    def get_nome(self):
        return self.__nome
  
    def set_nif(self,nif):
        self.__nif=nif
  
    def get_nif(self):
        return self.__nif
  
    def set_password(self,password):
        self.__password=password
  
    def get_password(self):
        return self.__password


##########################################################################################################################
# Adicionando uma despesa a lista de despesas
    
    def adicionar_despesa(self,data: str,categoria: str,valor: float,descDespesa: str):
                no_actual=self.__listaDespesas.head
                valor_total: float = 0.0
                data_inserida = datetime.strptime(data,"%d/%m/%Y")
                n: int=0
                while no_actual is not None:            
                    if data_inserida.strftime("%m/%Y") in no_actual.element.get_data():
                        valor_total += no_actual.element.get_valor() #Acumula o valor dos gastos de um determinado mês que esteja na lista  
                        
                        if valor_total >= self.__orcamento*0.8 and valor_total < self.__orcamento:
                           n=0 
                        elif valor_total == self.__orcamento:
                           n+=1   
                    no_actual=no_actual.next_node
                #--------------------------------------------------------------------  
                if self.__orcamento >= valor_total: #Verifica se os gastos de um determinado mês superam o orçamento    
                   AddDespesa = Despesas(data_inserida,categoria,valor,descDespesa)
                   self.__listaDespesas.insert_last(AddDespesa)
                   #print('Despesa adicionada')
                   messagebox.showinfo('Despesa','Despesa adicionada com sucesso')
                   
                elif n==0:
                   AddDespesa = Despesas(data_inserida,categoria,valor,descDespesa)
                   self.__listaDespesas.insert_last(AddDespesa)
                  # print('Despesa adicionada')
                   messagebox.showinfo('Despesa','Despesa adicionada com sucesso')
                   messagebox.showwarning('Alerta','O valor total das despesas está aproximar-se do orçamento')
                   #print('Alerta: O valor total das despesas está aproximar-se do orçamento')
                
                elif n>0:
                   AddDespesa = Despesas(data_inserida,categoria,valor,descDespesa)
                   self.__listaDespesas.insert_last(AddDespesa)
                  # print('Despesa adicionada') 
                   #print('Alerta: Já atingiste o limite do orçamento') 
                   messagebox.showinfo('Despesa','Despesa adicionada')
                   messagebox.showwarning('Alerta','Já atingiste o limite do orçamento')
                
                elif self.__orcamento is None:
                   # print('Alerta: Não foi definido um orçamento')   
                    messagebox.showwarning('Alerta','Não foi definido um orçamento')
                
                else:
                   # print('O valor(Eur) execede o limite do orcamento')   
                    messagebox.showerror('Atenção','O valor(Eur) excede o limite do orçamento, não pode ser adcicionada mais despesas')
    
#############################################################################################################################
    
# Consulta das despesas com tabela para lista ligada
# O objectivo é usar TDA'S dicionarios

    def consulta_listaDespesa_tabela(self):
        tabela=listaLigada()
        dicionario=dict() 

        no_actual=self.__listaDespesas.head
        
        while no_actual is not None:
            
            dicionario['categoria'] = no_actual.element.get_categoria()
            dicionario['Descrição da despesa'] = no_actual.element.get_descricaoDespesa()
            dicionario['Valor(Eur)'] = no_actual.element.get_valor()
            dicionario['Data'] = no_actual.element.get_data()
            
            tabela.insert_last(dicionario)   
            
            no_actual=no_actual.next_node  

        return pd.DataFrame(tabela)       
####################################################################################################################################

   
# Consulta na lista ligada         
    def consulta_listaDespesas_grafico(self):
        fig , ax = plt.subplots()
        no_actual = self.__listaDespesas.head
        lista_aux = listaLigada()

        while no_actual is not None:
            lista_aux.insert_last(no_actual.element.get_valor())
            no_actual=no_actual.next_node
        
        valores_np = np.array(lista_aux)
        ax.bar(self.__listaDespesas.get_first(),valores_np[0])

        no_actual = self.__listaDespesas.head #Recebe o 2º nó da lista
        i = 0
        while no_actual is not None:    # Percorre a lista ligada apartir do 2º nó, assim como no metodo "consulta_despesas_grafico(self)" acima
            if i>0:
              ax.bar(no_actual.element.get_categoria(),valores_np[i],bottom=valores_np[:i].sum(axis=0))
            no_actual = no_actual.next_node 
            i += 1

        ax.set_title('Gráfico de barras empilhadas')
        ax.set_xlabel('Categorias')
        ax.set_ylabel('Valores')  
        fig.show()    


#############################################################################################################################

# Filtrar dados por categoria da lista ligada

 
    def filtrar_listaDespesa(self):
        categorias=dict()
        no_actual = self.__listaDespesas.head
        lista_categorias = listaLigada()

        while no_actual is not None:
            if no_actual.element.get_categoria() in categorias:
                categorias[no_actual.element.get_categoria()]+=no_actual.element.get_valor()
            else:
                categorias[no_actual.element.get_categoria()]=no_actual.element.get_valor()    
            no_actual=no_actual.next_node
        
        for catg,valor in categorias.items():
            despesa = Despesas(None,catg,valor,None)
            lista_categorias.insert_last(despesa)
        
        lista_categorias.head = lista_categorias.mergesort()
        return lista_categorias     

#########################################################################################################################
 # Analisa histórico de despesas
    
    def analisa_historico_despesas(self):
        no_actual = self.__listaDespesas.head
        soma_valores = {}
        contador_valores_categoria = {}

        while no_actual is not None:
            
            if no_actual.element.get_categoria() not in soma_valores:
                soma_valores[no_actual.element.get_categoria()] = 0
                contador_valores_categoria[no_actual.element.get_categoria()] = 0 
                
            soma_valores[no_actual.element.get_categoria()] += no_actual.element.get_valor()
            contador_valores_categoria[no_actual.element.get_categoria()] += 1

            no_actual = no_actual.next_node
        media_por_categoria = {}
        
        for categoria in soma_valores:
            media_por_categoria[categoria] = soma_valores.get(categoria)/contador_valores_categoria.get(categoria) 

        listaDespeas_media = listaLigada()

        for catg, media in soma_valores.items():
            despesa = Despesas(None,catg,media,None)
            listaDespeas_media.insert_last(despesa)

        listaDespeas_media.head = listaDespeas_media.mergesort() 
        tamanho_lista = listaDespeas_media.size()

        if tamanho_lista == 1 or tamanho_lista == 2:
            
            return listaDespeas_media.get_last()# Retorna o último elemento da lista de cdespesas com médias 

        elif tamanho_lista > 2 :
            lista_maiores_gastos = listaLigada()
            no_corrente = listaDespeas_media.head
            maior_na_lista = listaDespeas_media.get_last()

            while no_actual is not None:#Busca os elementos da lista que têm uma percentagem maior ou igual à 50% que a do último vaor da lista com as médias já ordenas
                
                if no_corrente.element.get_valor() >=  maior_na_lista.get_valor()*0.5:
                
                    lista_maiores_gastos.insert_last(no_corrente.element) 
                
                no_corrente = no_corrente.next_node

            return lista_maiores_gastos    

           # ATT: A função retorna ou uma lista ligada ou uma única despesa 

       
#########################################################################################################################
 #   Ordenação da linkedlist 
    def Ordena_listaDespesas(self):
        self.__listaDespesas.head=self.__listaDespesas.mergesort()

#########################################################################################################################
# Filtração da lista por periodo de tempo
    def filtra_listaDespesas_periodo(self,data_inicio,data_fim):
        listaDespesas_filtrada=listaLigada()
        
        if type(data_inicio) is not datetime or type(data_fim) is not datetime:    
            data_inicio = datetime.strptime(data_inicio,"%d/%m/%Y")
            data_fim = datetime.strptime(data_fim,"%d/%m/%Y")

        no_actual=self.__listaDespesas.head
        while no_actual is not None:
            if data_inicio <= no_actual.element.get_data() or no_actual.element.get_data() <= data_fim:
                listaDespesas_filtrada.insert_last(no_actual.element)

            no_actual = no_actual.next_node 
        return listaDespesas_filtrada        
