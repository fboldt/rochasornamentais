import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_json('data/processeddata.json')

# title, journal, references
df_journals = df[['title', 'journal', 'references']].copy()

lista_journals = []
for i in range(len(df_journals)):
    lista_journals.append(df_journals.journal[i])
lista_journals = sorted(list(dict.fromkeys(lista_journals)))

df_journals.dropna(inplace=True)

# Criando os vértices
lista_pairs = []
for index, row in df_journals.iterrows():
    for index2, row2 in df_journals.iterrows():
        if row['title'] in row2['references']:
            lista_pairs.append((row['journal'], row2['journal']))

# Plotando o grafo
fig = plt.figure(figsize=(12, 12))
ax = plt.subplot(111)
ax.set_title('Graph - Shapes', fontsize=10)

G = nx.DiGraph()
G.add_edges_from(lista_pairs)
pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=1500, node_color='yellow',
        font_size=12, font_weight='bold', with_labels=True)

plt.tight_layout()
plt.savefig("./plot/map_fontes_periodicos.png", format="PNG")
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
H.add_edges_from(lista_pairs)
pos = nx.spring_layout(H)
nx.draw(H, pos, node_size=1500, node_color=color_map,
        font_size=12, font_weight='bold', with_labels=True)

plt.tight_layout()
plt.savefig("./plot/mapeamento_fontes_periodico_comunity.png", format="PNG")
# plt.show()