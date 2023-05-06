from abc import ABC
from List.Iterator import*

class IteradorFilho(Iterator):
    def __init__(self,colecao):
        self._colecao = colecao
        self._indice = 0
        #Os atributos ao invés de estarem privados __ estam protegidos _

    def has_next(self):
        return self._indice < len(self._colecao)

    def get_next(self):
        if not self.has_next():
            return None
        valor = self._colecao[self._indice]
        self._indice += 1
        return valor

    def rewind(self):
        self._indice = 0    
    