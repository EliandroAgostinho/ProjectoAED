from model.List.List import*
from model.List.Nodes import*

class listaLigada(List):
    def __init__(self):
        self.head = None
        self.size = 0 # ATT: O size é uma palavra reservada

    def is_empty(self):
        return self.head is None

    def size(self):
        return self.size

    def get_first(self):
        if self.head is None:
            raise Exception("Lista vazia")
        return self.head.get_element()


    def get_last(self):
        if self.head is None:
            raise Exception("Lista vazia")
        node = self.head
        while node.get_next_node() is not None:
            node = node.get_next_node()
        return node.get_element()

    def get(self, posicao):
        if posicao < 0 or posicao >= self.size:
            #raise Exception("Posição inválida")
            return None
        node = self.head
        for i in range(posicao):
            node = node.next_node
        return node.element

    def find(self, elemento):
        node = self.head
        posicao = 0
        while node is not None:
            if node.get_element() == elemento:
                return posicao
            node = node.get_next_node()
            posicao += 1
        return -1
    
    def find_username(self, username):
        node = self.head
        posicao = 0
        while node is not None:
            if node.element.get_nome() == username:
                return posicao
            node = node.next_node
            posicao += 1
        return -1
    

    def insert(self, elemento, posicao):
        if posicao < 0 or posicao > self.size:
            raise Exception("Posição inválida")
        if posicao == 0:
            self.insert_first(elemento)
        elif posicao == self.size:
            self.insert_last(elemento)
        else:
            node = self.head
            for i in range(posicao - 1):
                node = node.get_next_node()
            new_node = SingleListNode(elemento, node.get_next_node())
            node.set_next_node(new_node)
            self.size += 1

            
    def insert_first(self, elemento):
        node = SingleListNode(elemento, self.head)
        self.head = node
        self.size += 1

    def insert_last(self, elemento):
        if self.head is None:
            self.insert_first(elemento)
        else:
            node = self.head
            while node.get_next_node() is not None:
                node = node.get_next_node()
            new_node = SingleListNode(elemento, None)
            node.set_next_node(new_node)
            self.size += 1

    
    def remove_first(self):
        if self.head is None:
            raise Exception("Lista vazia")
        elemento = self.head.get_element()
        self.head = self.head.get_next_node()
        self.size -= 1
        return elemento

    def remove_last(self):
        if self.head is None:
            raise Exception("Lista vazia")
        if self.size == 1:
            return self.remove_first()
        node = self.head
        while node.get_next_node().get_next_node() is not None:
            node = node.get_next_node()
        elemento = node.get_next_node().get_element()
        node.set_next_node(None)
        self.size -= 1
        return elemento

    def remove(self, posicao):
        if posicao < 0 or posicao >= self.size:
            raise Exception("Posição inválida")
        if posicao == 0:
            return self.remove_first()
        if posicao == self.size - 1:
            return self.remove_last()
        node = self.head
        for i in range(posicao - 1):
            node = node.get_next_node()
        elemento = node.get_next_node().get_element()
        node.set_next_node(node.get_next_node().get_next_node())
        self.size -= 1
        return elemento

    def make_empty(self):
        self.head = None
        self.size = 0

    def iterator(self):
        node = self.head
        while node is not None:
            yield node.get_element()
            node = node.get_next_node()

 #########################################################################################   
    def divede_em_duas_partes(self): 
        rapido=self.head
        lento=self.head

        while rapido.next_node and rapido.next_node.next_node:
            rapido=rapido.next_node.next_node
            lento=lento.next_node 
     
        metade_direita = listaLigada()
        metade_direita.head=lento.next_node
     
        lento.next_node=None
     
        metade_esquerda = listaLigada()
        metade_esquerda.head = self.head

        return metade_esquerda,metade_direita

#########################################################################################
    def merge(self,mtd_esquerda,mtd_direita):
        lista_ordenada = listaLigada()
        
        if mtd_esquerda is None:
            return mtd_direita

        if mtd_direita is None:
            return mtd_esquerda

        if mtd_esquerda.element.get_valor() <= mtd_direita.element.get_valor():
            lista_ordenada.head = mtd_esquerda
            lista_ordenada.head.next_node = self.merge(mtd_esquerda.next_node,mtd_direita) 

        else:
            lista_ordenada.head = mtd_direita
            lista_ordenada.head.next_node =self.merge(mtd_esquerda,mtd_direita.next_node) 

        return lista_ordenada.head   

###################################################################################################
    def mergesort(self):
        if self.head is None or self.head.next_node is None:
            return self.head

        metade_esquerda , metade_direita = self.divede_em_duas_partes()

        metade_esquerda = metade_esquerda.mergesort()
        metade_direita = metade_direita.mergesort()

        return self.merge(metade_esquerda,metade_direita)             



