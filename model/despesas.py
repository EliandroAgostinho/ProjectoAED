from pandas import*
from numpy import*
from datetime import datetime

class Despesas:

    def __init__(self,data: str,categoria: str,valor: float,descDespesa: str):
        self.__data = datetime.strptime(data,"%d/%m/%Y")
        self.__categoria:str = categoria
        self.__valor:float = valor
        self.__descricaoDespesa:str = descDespesa
    
# Metodos especiais getters e setters

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def get_categoria(self):
        return self.__categoria

    def set_categoria(self, categoria):
        self.__categoria = categoria

    def get_valor(self):
        return self.__valor

    def set_valor(self, valor):
        self.__valor = valor     

    def set_descricaoDespesa(self,descDespesa):
        self.__descricaoDespesa = descDespesa

    def get_descricaoDespesa(self):
        return self.__descricaoDespesa     

        
