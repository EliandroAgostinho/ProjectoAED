from despesas import*
from typing import Type
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Utilizador:
    

    def __init__(self,nome: str,nif: int,password: str):
        self.__nome:str = nome
        self.__nif:int = nif
        self.__password:str = password
        self.__despesas: list[Despesas] = []

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
                self.__despesas.append(AddDespesa)
        

#############################################################################################################################
#  consulta das despesas com tabela ou gráficos 

    def consulta_despesas_tabela(self):   # Retorna a tabela com os dados das despesas 
        tabela_dispesas = [{'Categoria':dp.get_categoria,'Descrição da despesa':dp.get_descricaoDespesa,'Valor(Eur)':dp.get_valor,'Data':dp.get_data} for dp in self.__despesas]
        #pd.DataFrame([dp.__dict__ for dp in self.__despesas])

        return pd.DataFrame(tabela_dispesas)

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
         

#############################################################################################################################
#Filtração de dados por categoria 

    def filtrar_despesas(self,categoria:str):
        pass 

##############################################################################################################################
#Ordenação da lista de despesas do utilizador com o mergesort
    
    def ordena_despesas_com_mergesort(self,lista_despesa:list[Despesas]):
        self.__despesas=lista_despesa
        
        if len(self.__despesas) <= 1:
            return self.__despesas

        meio = len(self.__despesas) // 2
        
        metade_esquerda: list[Despesas] = self.__despesas[:meio]
        metade_direita: list[Despesas] = self.__despesas[meio:]
        
        metade_esquerda = self.ordena_despesas_com_mergesort(metade_esquerda)
        metade_direita = self.ordena_despesas_com_mergesort(metade_direita)

        self.__despesas: list[Despesas] = []
        i_esquerda=i_direita=0

        while(i_esquerda<len(metade_esquerda) and i_direita<len(metade_direita)):
        
            if metade_esquerda[i_esquerda].get_valor <= metade_direita[i_direita].get_valor():
                self.__despesas.append(metade_esquerda[i_esquerda])
                i_esquerda+=1
        
            else:
                self.__despesas.append(metade_direita[i_direita])
                i_direita+=1

        self.__despesas += metade_esquerda[i_esquerda:]
        self.__despesas += metade_direita[i_direita:]
        return self.__despesas        

 #########################################################################
 #    
    def Ordena_Despesas(self):
        def mergesort(lista):
            if len(lista) <= 1:
                return lista

            meio=len(lista) // 2
            metade_esquerda: list[Despesas]=lista[:meio]
            metade_direita: list[Despesas]=lista[meio:]

            metade_esquerda = mergesort(metade_esquerda)
            metade_direita = mergesort(metade_direita)

            return merge(metade_esquerda,metade_direita)

        def merge(metd_esquerda: list[Despesas],met_direita: list[Despesas]):    
          resultado: list[Despesas]=[]
          i_esquerdo=i_direito=0

          while i_esquerdo < len(metd_esquerda) and i_direito < len(met_direita):
            if metd_esquerda[i_esquerdo].get_valor() <= met_direita[i_direito].get_valor():
                 resultado.append(metd_esquerda[i_esquerdo])
                 i_esquerdo += 1

            else:
                resultado.append(met_direita[i_direito])
                i_direito += 1

          if i_esquerdo < len(metd_esquerda[i_esquerdo]):
            resultado.extend(metd_esquerda[i_esquerdo:])

          if i_direito < len(met_direita[i_direito]):
            resultado.extend(met_direita[i_direito:])            

          return resultado

        self.__despesas=mergesort(self.__despesas)
       
