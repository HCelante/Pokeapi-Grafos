import json
import os
import networkx as nx
import matplotlib.pyplot as plt
import sys
from networkx import immediate_dominators, degree
#funcao que imprime o tipo de pokemon mais forte
def strongest_type(g):
    max_n = 0
    suma = 0

    for i in g.nodes:
        for j in g.neighbors(i):
            suma +=1
        if suma > max_n:
            typeofpkm = i
            max_n = suma

        suma  = 0
    print typeofpkm


def tipomaisfraco(g):
    min_n = 99
    max_n = 0
    suma = 0
    degreae = 0
    for i in g.nodes:
        degreae = g.degree(i)
        for j in g.neighbors(i):
            suma +=1
        if (suma < min_n) and (degreae > max_n):
            typefpkm = i
            min_n = suma
            
            #print degreae
        suma  = 0
    print typefpkm


#funcao de imprime todos os nos conectados ao vertice da busca
def get_dmg_to(typeofpkm, g):
    list_neighbors = g.neighbors(typeofpkm)
    
    for i in list_neighbors:
        print (i)

#funcao que seta os vertices do grafo dd
def set_digraph_dd(dd, poke_json, poke_damage_json):
    
    for i in range (len(poke_json['results'])):
        for j in range (len(poke_damage_json[i]['damage_relations']['double_damage_to'])):
            dd.add_edge(str(poke_json['results'][i]['name']), str(poke_damage_json[i]['damage_relations']['double_damage_to'][j]['name']), weight='1')

#funcao que seta os vertices do grafo hd
def set_digraph_hd(hd, poke_json, poke_damage_json):
    
    for i in range (len(poke_json['results'])):
        for j in range (len(poke_damage_json[i]['damage_relations']['half_damage_to'])):
            hd.add_edge(str(poke_json['results'][i]['name']), str(poke_damage_json[i]['damage_relations']['half_damage_to'][j]['name']), weight='0.5')

#funcao que seta os vertices do grafo nd
def set_digraph_nd(nd, poke_json, poke_damage_json):
    
    for i in range (len(poke_json['results'])):
        for j in range (len(poke_damage_json[i]['damage_relations']['no_damage_to'])):
            nd.add_edge(str(poke_json['results'][i]['name']), str(poke_damage_json[i]['damage_relations']['no_damage_to'][j]['name']), weight='0')

#funcao que recebe a lista de tipos de pokemons e as lista de urls
def get_edges(poke_json, list_urls):
    url = "pokeapi/data"
    #concatena os enderecos(urls) de cada tipo dentro do index.json de types
    type_url_list = []
    
    for i in range (len(list_urls)):
        type_url_list.append(url + os.path.join(list_urls[i], "index.json"))
    
    #faz a abertura de cada arquivo numa lista
    type_file_list = []
    for i in range (len(type_url_list)):
        type_file_list.append(open(type_url_list[i], "r"))
    
    #preenche uma lista de json de cada tipo de pokemon
    poke_damage_json = []
    for i in range (len(type_file_list)):
        poke_damage_json.append(json.load(type_file_list[i]))
    
    return poke_damage_json
    
#funcao na qual vai criar os vertices do grafo
#recebe como paramento o arquivo json e a estrutura do grafo
def set_vertex(poke_json, dd, hd, nd):
    list_urls =[]
    
    #laco que adiciona o no(vertice) na estrutura do grafo
    #e lista de urls, para conseguir as informacoes de dano do pokemon
    for i in range (len(poke_json['results'])):
        dd.add_node(str(poke_json['results'][i]['name']),type=str(poke_json['results'][i]['name']))
        hd.add_node(str(poke_json['results'][i]['name']),type=str(poke_json['results'][i]['name']))
        nd.add_node(str(poke_json['results'][i]['name']),type=str(poke_json['results'][i]['name']))
        list_urls.append(poke_json['results'][i]['url'])
    return list_urls
    
def main():
    #incializacao dos grafos
    dd = nx.DiGraph()
    hd = nx.DiGraph()
    nd = nx.DiGraph()


    with open("pokeapi/data/api/v2/type/index.json", "r") as f:
        poke_json = json.load(f)

    #set_vertex retorna a lista de urls do json    
    list_urls = set_vertex(poke_json, dd, hd, nd)

    #get edges retorna uma lista poke_damage_json, com todos os json de dano de cada tipo
    poke_damage_json = get_edges(poke_json, list_urls)

    #seta os vertices de cada digrafo, sendo um para double damage(dd), half damage(hd), no_damage(nd)
    set_digraph_dd(dd, poke_json, poke_damage_json)
    set_digraph_hd(hd, poke_json, poke_damage_json)
    set_digraph_nd(nd, poke_json, poke_damage_json)
    
    #para efetuar a busca, deve entrar o tipo do pokemon (electric, steel, bug, ...) e o tipo de relacao de dano (dd, hd, nd)
    typeofdmg = '0'
    if (len(sys.argv) == 3):
        typeofpkm = sys.argv[1]
        typeofdmg = sys.argv[2]
    else :
        strg = sys.argv[1]

    #chamada da funcao que imprime na tela os tipos de pokemons referente a busca do usuario
    while True:
        if (typeofdmg == 'dd'): #encontra dd
            get_dmg_to(typeofpkm, dd)
            #desenha o grafo
            nx.draw_shell(dd, with_labels=True, edge_color='b', font_weight='bold', font_size = 10, width=2)
            plt.show()
            break
        elif (typeofdmg == 'hd'): #encontra hd
            get_dmg_to(typeofpkm, hd)
            #desenha o grafo
            nx.draw_shell(hd, with_labels=True, edge_color='purple', font_weight='bold', font_size = 10, width=2)
            plt.show()
            break
        elif (typeofdmg == 'nd'): #encontra nd
            get_dmg_to(typeofpkm, nd)
            #desenha o grafo
            nx.draw_shell(nd, with_labels=True, font_weight='bold', font_size = 10, width=2)
            plt.show()
            break
        elif (strg == 'strg'):
            strongest_type(dd)
            #desenha o grafo
            nx.draw_shell(dd, with_labels=True, edge_color='b', font_weight='bold', font_size = 10, width=2)
            plt.show()
            break
        elif(strg == 'weaker'):
            tipomaisfraco(dd)
            nx.draw_shell(dd, with_labels=True, edge_color='b', font_weight='bold', font_size = 10, width=2)
            plt.show()
            break

        else:
            print ("relacao de dano nao existente, use dd, hd ou nd")
            typeofdmg = raw_input("Digite novamente: ")

    
if __name__ == "__main__":
    main()
