import pandas as pd
import itertools
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_json('data/processeddata.json')
df_keywords = df[['keywords', 'author_keywords']].copy()
df_keywords.fillna(value='', inplace=True)

df_keywords['all_keywords'] = None
df_keywords['keywords_pairs'] = None

# Juntando os dois tipos de keywords
# Tirando as duplicatas
# Criando os pares de palavras-chave
all_keywords = []
all_pairs = []
for index, row in df_keywords.iterrows():
    row['keywords'] = row['keywords'].lower()
    row['author_keywords'] = row['author_keywords'].lower()

    row['all_keywords'] = row['keywords'].split(
        sep=';  ') + row['author_keywords'].split(sep=';  ')
    row['all_keywords'] = sorted(list(dict.fromkeys(row['all_keywords'])))

    while '' in row['all_keywords']:
        row['all_keywords'].remove('')

    if len(row['all_keywords']) >= 2:
        row['keywords_pairs'] = list(
            itertools.combinations(row['all_keywords'], 2))

    all_keywords += row['all_keywords']
    if row['keywords_pairs'] != None:
        all_pairs += row['keywords_pairs']

# Nós do grafo
all_keywords = list(dict.fromkeys(all_keywords))

# Vértices do grafo
vertices_dic = dict((x, all_pairs.count(x)) for x in set(all_pairs))
# Iloni só pegou os que tinham mais de 5 coocorrencias
vertices_dic_limite = {key: val for key,
                       val in vertices_dic.items() if val >= 5}
vertices = list(vertices_dic_limite.keys())

# Printando o grafo
# G = nx.Graph()
# G.add_edges_from(vertices)
# nx.draw(G, with_labels=True, font_weight='bold')

fig = plt.figure(figsize=(12, 12))
ax = plt.subplot(111)
ax.set_title('Graph - Shapes', fontsize=10)

G = nx.DiGraph()
G.add_edges_from(vertices)
pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=1500, node_color='yellow',
        font_size=12, font_weight='bold', with_labels=True)

plt.tight_layout()
plt.savefig("./plot/coocorrencia.png", format="PNG")
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
H.add_edges_from(vertices)
pos = nx.spring_layout(H)
nx.draw(H, pos, node_size=1500, node_color=color_map,
        font_size=12, font_weight='bold', with_labels=True)

plt.tight_layout()
plt.savefig("./plot/coocorrencia_comunity.png", format="PNG")
# plt.show()