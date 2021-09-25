import csv

# classe grafo - Cria o grafo, importa os dados da planilha csv, adiciona e conecta os vertices (usuários)
class Grafo():
    def __init__(self):
        self.adjacencia = {}
    
    def adiciona(self, vertice):
        self.adjacencia[vertice] = {}
    
    def conecta(self, origem, destino, peso):
        self.adjacencia[origem][destino] = peso
       
    def cria_grafo(self):
        g = Grafo()
        #importa o arquivo csv (usuarios)
        with open('usuarios.csv', encoding='utf-8') as usuarios:
            tabela_csv = csv.reader(usuarios, delimiter=',', quoting=csv.QUOTE_NONE)

            for linha in tabela_csv:
                user_id_origin = linha[1]
                g.adiciona(user_id_origin)

        #importa o arquivo csv (conexões), contendo o username e as respectivas pessoas que este user segue
        with open('conexoes.csv', encoding='utf-8') as conexoes:
            conexoes_csv = csv.reader(conexoes, delimiter=',', quoting=csv.QUOTE_NONE)

            for linha in conexoes_csv:
                g.conecta(str(linha[0]), str(linha[1]), linha[2])

        return g
    
    # encontra o caminho entre um usuário X e usuário Y   
    def encontra_caminho(self, origem, destino):
        fila = [origem] # fila inicia-se com o usuário origem
        visitados = []  # nesta lista serão armazenados os usuáriso já visitados pelo código
        predecessor = {origem: None}
        
        while len(fila) > 0:
            primeiro_elemento = fila[0]
            fila = fila[1:]
            visitados.append(primeiro_elemento)
            for adjacente in self.adjacencia[primeiro_elemento].keys():
                if adjacente == destino:
                    pred = primeiro_elemento
                    caminho_invertido = [destino]
                    while pred is not None:
                        caminho_invertido.append(pred)
                        pred = predecessor[pred]
                    
                    caminho = ''
                    for no in caminho_invertido[::-1]:
                        caminho += f'{no} -> '
                    return caminho[:-3]
                
                if adjacente not in fila and adjacente not in visitados:
                    predecessor[adjacente] = primeiro_elemento
                    fila.append(adjacente)
                    
        # caso não exista caminho entre a origem e o destino, retorna False    
        return False
    
    # exibe o número de pessoas que o usuário selecionado segue 
    def exibe_Nrpessoas_usuario_segue(self, usuario):
        nr_seguidores = 0
        for chave in self.adjacencia[usuario].keys():
            for i in self.adjacencia[usuario]:
                nr_seguidores += 1       
            return print(f' O(A) usuario(a) {usuario} segue {nr_seguidores} pessoas.')
    
    # exibe o número de seguidores que o usuário possui 
    def exibe_seguidores_usuario_possui(self, usuario):
        nr_seguidores = 0
        for chave in self.adjacencia.keys():
            if usuario in self.adjacencia[chave]:
                nr_seguidores += 1       
        return print(f' O(A) usuario(a) {usuario} possui {nr_seguidores} seguidores.')
    
    # exibe os n top influencers, baseado no número de seguidores que este usuário possui
    def encontra_top_influencer(self, top_influencers):
        dict_nr_seguidores = {} # dicionário vazio para armazenar o usuário e q quantidade de seguidores
        for chave in self.adjacencia:
            seguidores = 0
            for linha in self.adjacencia.items():
                for item in linha[1].items():
                    if chave in item:
                        seguidores += 1
            dict_nr_seguidores[chave] = seguidores
        
        # transformando o dicionario em tupla, com o usuario e a quantidade de seguidores
        lista_nr_seguidores = list(dict_nr_seguidores.items())
        
        # Organiza as tuplas com o Bubble Sort
        for i in range(len(lista_nr_seguidores)):
            for j in range(len(lista_nr_seguidores)):
                if lista_nr_seguidores[j][1] < lista_nr_seguidores[i][1]:
                    lista_nr_seguidores[i], lista_nr_seguidores[j] = lista_nr_seguidores[j], lista_nr_seguidores[i]

        # criação de string para melhor visualização do print dos top influcencers
        str_top_influcencers = ''
        for item in lista_nr_seguidores[:top_influencers]:
            str_top_influcencers += str(item[0]) + ', com ' + str(item[1]) + " seguidores; "

        return print(f'Os {top_influencers} top influencers são: {str_top_influcencers}')
                        
    # exibe os melhores amigos de determinado usuário                    
    def melhores_amigos(self, usuario):
        amigos = list(self.adjacencia[usuario].items()) # seleciona, dentro do dict, os amigos do usuário
        lista_melhor_amigo = []
        lista_amigos_comum = []
        
        # classifica os melhores amigos, através do peso dado (2 = melhor amigo, 1 = amigo "comum")
        for item in amigos:
            if item[1] == "2":
                lista_melhor_amigo.append(item[0])
            else:
                lista_amigos_comum.append(item[0])
        
        # ordenando a lista de melhores amigos    
        for i in range(len(lista_melhor_amigo)):
            for j in range(len(lista_melhor_amigo)):
                if lista_melhor_amigo[i] < lista_melhor_amigo[j]:
                    lista_melhor_amigo[i], lista_melhor_amigo[j] = lista_melhor_amigo[j], lista_melhor_amigo[i]
        
        # ordenando a lista de amigos "comuns"        
        for i in range(len(lista_amigos_comum)):
            for j in range(len(lista_amigos_comum)):
                if lista_amigos_comum[i] < lista_amigos_comum[j]:
                    lista_amigos_comum[i], lista_amigos_comum[j] = lista_amigos_comum[j], lista_amigos_comum[i]
        
        # esta lista contém tanto os melhores amigos quanto os amigos comuns, ambos classificados em ordem alfabética
        lista_amigos_final = lista_melhor_amigo + lista_amigos_comum
        
        # neste print, optei por separar em duas listas os melhores amigos e, em seguida, os amigos comuns. 
        # se necessário, pode-se utilizar a lista acima (lista_amigos_final), que contém todos os amigos.
        return print(f'Os melhores amigos do usuario {usuario} são: {lista_melhor_amigo}\nOs demais amigos do usuario {usuario} são {lista_amigos_comum}')
        
                