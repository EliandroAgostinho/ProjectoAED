import json
import datetime
from model.listaLigada import*
from model.despesas import*
from model.utilizador import*
import io


class ManipulaArquivos:
    
    def limpar_ficheiro(self):
        with open("dadosSCDM.json",'w') as ficheiro:
            ficheiro.write("")

    #################################################################################################        

    def salvar_dados_em_json(self,lista_clientes: listaLigada = None):
        dados_existentes = self.ler_ficheiro_json()  

        dados = {
            'lista de clientes': []
        }  
    #######################################################################
        no_atual = lista_clientes.head

        while no_atual is not None:# Transformar um objecto cliente em um dicionario

            if no_atual.get_element().get_orcamento():
                dados_clientes = {
                'nome':no_atual.get_element().get_nome(),
                'nif':no_atual.get_element().get_nif(),
                'password':no_atual.get_element().get_password(),
                'orcamento':no_atual.get_element().get_orcamento(),
                'despesas':[]
               }
            else:
                dados_clientes = {
                'nome':no_atual.get_element().get_nome(),
                'nif':no_atual.get_element().get_nif(),
                'password':no_atual.get_element().get_password(),
                'orcamento':0.0,
                'despesas':[]
               }
            
            no_atual_despesas = no_atual.get_element().get_listaDespesas().head
            
            while no_atual_despesas is not None:
                dados_despesas = {
                    'categoria':no_atual_despesas.get_element().get_categoria(),
                    'descricao':no_atual_despesas.get_element().get_descricaoDespesa(),
                    'valor':no_atual_despesas.get_element().get_valor(),
                    'data':no_atual_despesas.get_element().get_data().strftime("%d/%m/%Y")
                }
                dados_clientes['despesas'].append(dados_despesas)

                no_atual_despesas = no_atual_despesas.next_node
                ###############################################
            no_clientes_existentes = dados_existentes.head
            clinte_existe = None

            while no_clientes_existentes is not None:
                if no_clientes_existentes.element.get_nome()==no_atual.get_element().get_nome() and no_clientes_existentes.element.get_nif()==no_atual.get_element().get_nif():
                    clinte_existe: Utilizador = no_clientes_existentes.element
                    break

                no_clientes_existentes = no_clientes_existentes.next_node

            if clinte_existe is not None:
                dados_cliente_existente ={
                'nome':clinte_existe.get_nome(),
                'nif':clinte_existe.get_nif(),
                'password':clinte_existe.get_password(),
                'orcamento':clinte_existe.get_orcamento(),
                'despesas':[]
                }

                clinte_existe_no_despesas = clinte_existe.get_listaDespesas().head
               
                while clinte_existe_no_despesas is not None:
               
                     dados_despesas_clinte_existente = {
                    'categoria':clinte_existe_no_despesas.get_element().get_categoria(),
                    'descricao':clinte_existe_no_despesas.get_element().get_descricaoDespesa(),
                    'valor':clinte_existe_no_despesas.get_element().get_valor(),
                    'data':clinte_existe_no_despesas.get_element().get_data().strftime("%d/%m/%Y")
                    }
                     
               
                     dados_cliente_existente['despesas'].append(dados_despesas_clinte_existente)

                     clinte_existe_no_despesas = clinte_existe_no_despesas.next_node

                dados_cliente_existente.update(dados_clientes) 

                dados['lista de clientes'].append(dados_cliente_existente)    
                

            else:     
                 dados['lista de clientes'].append(dados_clientes)
            
            no_atual = no_atual.next_node   

        with open("dadosSCDM.json",'w') as ficheiro: 
            json.dump(dados,ficheiro)
     
        
    
    ################################################################################################################
    def ler_ficheiro_json(self):
        dados = None

        try:
            with open("dadosSCDM.json",'r') as ficheiro:
               conteudo = ficheiro.read()
               if conteudo.strip():  # Verifica se o conteúdo não está vazio
                 ficheiro_io = io.StringIO(conteudo) 
                 dados = json.load(ficheiro_io)

                 lista_clientes = listaLigada()


                 if 'lista de clientes' in dados and dados['lista de clientes']:
                    for dados_clientes in dados['lista de clientes']:
                       cliente = Utilizador(dados_clientes['nome'],dados_clientes['nif'],dados_clientes['password'])   
                       cliente.set_orcamento(dados_clientes['orcamento'])

                       for dados_despesa in dados_clientes['despesas']:
                          cliente.adicionar_despesa(dados_despesa['data'],dados_despesa['categoria'],dados_despesa['valor'],dados_despesa['descricao'])

                       lista_clientes.insert_last(cliente)

                    return lista_clientes
              
               else:
                   
                   return listaLigada()

        except FileNotFoundError:   
                   
                   return listaLigada()
        
        except json.JSONDecodeError:
            
            return listaLigada()
        
               
    
    

    
    


                  