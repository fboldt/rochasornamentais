import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools

df = pd.read_json('data/processeddata.json')

# authors
df_authors = df[['author']].copy()
df_authors.dropna(inplace=True)

df_authors['lista_autores'] = None
df_authors['pares_autores'] = None

todos_autores = []
for i, row in df_authors.iterrows():
    row['author'] = row['author'].lower()
    row['lista_autores'] = row['author'].split(sep=' and ')
    row['lista_autores'] = sorted(list(dict.fromkeys(row['lista_autores'])))

    if len(row['lista_autores']) >= 2:
        row['pares_autores'] = list(
            itertools.combinations(row['lista_autores'], 2))

    if row['pares_autores'] != None:
        todos_autores += row['pares_autores']

# Vértices do grafo
vertices_dic = dict((x, todos_autores.count(x)) for x in set(todos_autores))
# só pegou quem participou em mais de um artigo
vertices_dic_limite = {key: val for key,
                       val in vertices_dic.items() if val >= 2}
vertices = list(vertices_dic_limite.keys())

# Plotando grafo
fig = plt.figure(figsize=(12, 12))
ax = plt.subplot(111)
ax.set_title('Graph - Shapes', fontsize=10)

G = nx.DiGraph()
G.add_edges_from(vertices)
pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=1500, node_color='yellow',
        font_size=12, font_weight='bold', with_labels=True)

plt.tight_layout()
plt.savefig("./plot/coautoria.png", format="PNG")
# plt.show()

# Dividindo em communities

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
        if node in node_groups[i] and (i % 8 == 0):
            color_map.append('blue')
        if node in node_groups[i] and (i % 8 == 1): 
            color_map.append('green')
        if node in node_groups[i] and (i % 8 == 2): 
            color_map.append('yellow')
        if node in node_groups[i] and (i % 8 == 3):
            color_map.append('red')
        if node in node_groups[i] and (i % 8 == 4):
            color_map.append('brown')
        if node in node_groups[i] and (i % 8 == 5): 
            color_map.append('purple')
        if node in node_groups[i] and (i % 8 == 6): 
            color_map.append('pink')
        if node in node_groups[i] and (i % 8 == 7):
            color_map.append('gray')

# Plotando grafo
fig = plt.figure(figsize=(12, 12))
ax = plt.subplot(111)
ax.set_title('Graph_clusters - Shapes', fontsize=10)

H = nx.DiGraph()
H.add_edges_from(vertices)
pos = nx.spring_layout(H)
nx.draw(H, pos, node_size=1500, node_color=color_map,
        font_size=12, font_weight='bold', with_labels=True)

plt.tight_layout()
plt.savefig("./plot/coautoria_comunity.png", format="PNG")
# plt.show()