import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re
import itertools

df = pd.read_json('data/processeddata.json')

# author, references
df_authors = df[['author', 'references']].copy()

# Criando nova coluna com os dados dos artigos da referencia
df_authors['references_articles'] = pd.DataFrame

for i, row in df_authors.iterrows():
    df_dados = pd.DataFrame(columns=['titulo', 'autores', 'revista'])

    # Lista de todos os artigos da referência
    if row['references'] != None:
        todos_aritgos = row['references'].split(sep='; ')

    # Lista dos artigos que foram publicados em revistas
    artigos_revista = []
    for artigo in todos_aritgos:
        if 'doi.org' in artigo:
            artigos_revista.append(artigo)

    # Pegar dados da lista de artigos de revistas:
    if len(artigos_revista) >= 1:
        for artigo in artigos_revista:
            revista = ''
            titulo = ''
            autores = ''
            pre_dado = re.split('\([1-2][0-9][0-9][0-9]\)', artigo)

            if len(pre_dado) == 2:
                revista = pre_dado[1].split(',', 1)
                if len(revista) == 2:
                    revista = revista[0].strip()

                titulo = pre_dado[0].rsplit(',', 1)
                if len(titulo) == 2:
                    titulo = titulo[1].strip()
                    autores = pre_dado[0].rsplit(',', 1)[0]
                    autores = autores.split('.,')
                    n_autores = []
                    for i in (range(len(autores) - 1)):
                        autores[i] += '.'
                    for autor in autores:
                        autor = autor.strip().lower()
                        n_autores.append(autor)
                    n_autores = sorted(list(dict.fromkeys(n_autores)))

            # Colocar informações no dataframe
            df_dados = df_dados.append(
                {'titulo': titulo, 'autores': n_autores, 'revista': revista}, ignore_index=True)
            row['references_articles'] = df_dados

df_authors['lista_autores'] = None
df_authors['pares_autores'] = None

vertices = []
for i, row in df_authors.iterrows():
    todos_autores = []
    if not (row['references_articles'].empty):
        for j, linha in row['references_articles'].iterrows():
            todos_autores += linha['autores']
        todos_autores = sorted(list(dict.fromkeys(todos_autores)))
        row['lista_autores'] = todos_autores

    if row['lista_autores'] != None:
        if len(row['lista_autores']) >= 2:
            row['pares_autores'] = list(
                itertools.combinations(row['lista_autores'], 2))

    if row['pares_autores'] != None:
        vertices += row['pares_autores']

# Vértices do grafo
vertices_dic = dict((x, vertices.count(x)) for x in set(vertices))
vertices_dic_limite = {key: val for key,
                       val in vertices_dic.items() if val >= 2}
vertices_grafo = list(vertices_dic_limite.keys())

# Plotando grafo
fig = plt.figure(figsize=(12, 12))
ax = plt.subplot(111)
ax.set_title('Graph - Shapes', fontsize=10)

G = nx.DiGraph()
G.add_edges_from(vertices_grafo)
pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=1500, node_color='yellow',
        font_size=12, font_weight='bold', with_labels=True)

plt.tight_layout()
plt.savefig("./plot/cocitacao_autores.png", format="PNG")
# plt.show()

#Dividindo em communities

def edge_to_remove(graph):
    G_dict = nx.edge_betweenness_centrality(graph)
    edge = ()

    # extract the edge with highest edge betweenness centrality score
    for key, value in sorted(G_dict.items(), key=lambda item: item[1], reverse = True):
        edge = key
        break

    return edge

def girvan_newman(graph):
    # find number of connected components
    sg = nx.connected_components(graph)
    sg_count = nx.number_connected_components(graph)

    while(sg_count == 1):
        graph.remove_edge(edge_to_remove(graph)[0], edge_to_remove(graph)[1])
        sg = nx.connected_components(graph)
        sg_count = nx.number_connected_components(graph)
    
    return sg

H = G.to_undirected()

# find communities in the graph
c = girvan_newman(H.copy())
# find the nodes forming the communities
node_groups = []

for i in c:
    node_groups.append(list(i))

color_map = []
for node in H:
    for i in range(len(node_groups)):
        if node in node_groups[i] and (i % 4 == 0):
            color_map.append('blue')
        if node in node_groups[i] and (i % 4 == 1): 
            color_map.append('green')
        if node in node_groups[i] and (i % 4 == 2): 
            color_map.append('yellow')
        if node in node_groups[i] and (i % 4 == 3):
            color_map.append('red')

# Plotando grafo
fig = plt.figure(figsize=(12, 12))
ax = plt.subplot(111)
ax.set_title('Graph_clusters - Shapes', fontsize=10)

H = nx.DiGraph()
H.add_edges_from(vertices_grafo)
pos = nx.spring_layout(H)
nx.draw(H, pos, node_size=1500, node_color=color_map,
        font_size=12, font_weight='bold', with_labels=True)

plt.tight_layout()
plt.savefig("./plot/coautoria_comunity.png", format="PNG")
# plt.show()