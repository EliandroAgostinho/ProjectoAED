from despesas import*
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from listaLigada import*
from datetime import datetime

class Utilizador:
    

    def __init__(self,nome: str,nif: int,password: str):
        self.__nome:str = nome
        self.__nif:int = nif
        self.__password:str = password
        self.__despesas: list[Despesas] = [] # Lista normal
        self.__listaDespesas=listaLigada() # Lista ligada

#################################################################################################################################
# Metodos getters e setters

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

    def set_despesas(self,despesas):
        self.__despesas.clear()
        self.__despesas=despesas

    def get_despesas(self):
        return self.__despesas    


##########################################################################################################################
# Adicionando uma despesa a lista de despesas
     
    def adicionar_despesa(self,data: str,categoria: str,valor: float,descDespesa: str):
                AddDespesa = Despesas(data,categoria,valor,descDespesa)
                self.__listaDespesas.insert_last(AddDespesa)
                self.__despesas.append(AddDespesa)# Apagar
        

#############################################################################################################################
#  consulta das despesas com tabela ou gráficos "Lista normal" 
# Tem dicionários

    def consulta_despesas_tabela(self):   # Retorna a tabela com os dados das despesas 
        tabela_dispesas = [{'Categoria':dp.get_categoria(),'Descrição da despesa':dp.get_descricaoDespesa(),'Valor(Eur)':dp.get_valor(),'Data':dp.get_data()} for dp in self.__despesas]
        #pd.DataFrame([dp.__dict__ for dp in self.__despesas])
        return pd.DataFrame(tabela_dispesas)

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
# Consulta na lista normal
# Não tem dicionários

    def consulta_despesas_grafico(self):
        fig , ax =plt.subplots()
        valores_np=np.array([dps.__valor for dps in self.__despesas])
        ax.bar(self.__despesas[0].__categoria,valores_np[0])
        
        for i in range(1,len(self.__despesas)):
            ax.bar(self.__despesas[i].__categoria,valores_np[i],bottom=valores_np[:i].sum(axis=0))
        
        ax.set_title('Gráfico de barras empilhadas')
        ax.set_xlabel('Categorias')
        ax.set_ylabel('Valores')  
        fig.show() 
        #plt.show() 
        # Tanto o comando fig.show() como plt.show() mostram servem para mostrar a figura 
        #fig.show() mostra uma figura especifica
        #plt.show() mostra a figura criada mais recentemente
        #Como só criamos uma figura a cada chamamento do metodo, então qualquer um dos 2 comandos serve para mostrar a figura

# Consulta na lista ligada         
    def consulta_listaDespesas_grafico(self):
        fig , ax =plt.subplots()
        no_actual=self.__listaDespesas.head
        lista_aux=[]

        while no_actual is not None:
            lista_aux.append(no_actual.element.get_valor())
            no_actual=no_actual.next_node
        
        valores_np = np.array(lista_aux)
        ax.bar(self.__listaDespesas.get_first(),valores_np[0])

        no_actual = self.__listaDespesas.head #Recebe o 2º nó da lista
        i = 0
        while no_actual is not None:    # Percorre a lista ligada apartir do 2º nó, assim como no metodo "consulta_despesas_grafico(self)" acima
            if i>0:
              ax.bar(no_actual.element.get_categoria(),valores_np[i],bottom=valores_np[:i].sum(axis=0))
            no_actual = no_actual.next_node 
            i=i+1

        ax.set_title('Gráfico de barras empilhadas')
        ax.set_xlabel('Categorias')
        ax.set_ylabel('Valores')  
        fig.show()    


#############################################################################################################################
#Filtração de dados por categoria da lista normal
#Tem dicionarios

    def filtrar_despesas(self):
        categorias={}
        for despesa in self.__despesas:
            if despesa.get_categoria() in categorias:
                categorias[despesa.get_categoria()]+=despesa.get_valor()
            else:
                categorias[despesa.get_categoria()]=despesa.get_valor()
        return categorias            

# Filtrar dados por categoria da lista ligada

 
    def filtrar_listaDespesa(self):
        categorias=dict()
        no_actual=self.__listaDespesas.head
        while no_actual is not None:
            if no_actual.element.get_categoria() in categorias:
                categorias[no_actual.element.get_categoria()]+=no_actual.element.get_valor()
            else:
                categorias[no_actual.element.get_categoria()]=no_actual.element.get_valor()    
            no_actual=no_actual.next_node
        
        return categorias

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
            if data_inicio <= no_actual.element.get_data() <= data_fim:
                listaDespesas_filtrada.insert_last(no_actual.element)

            no_actual = no_actual.next_node 
        return listaDespesas_filtrada        
