from constraint import *
import networkx as nx
import matplotlib.pyplot as plt
from backtracking import backtrackingSearch

G = nx.Graph()

nodelist=["WA", "NT", "Q", "SA", "NSW", "V", "T"]
domain_list=[1,2,3]

color_map = {1:'#ff0000', 2:'#00ff00', 3:'#0000ff'}


for i in nodelist:
	G.add_node(i, domain=domain_list)

G.nodes()
edges=[("WA","NT"),("WA","SA"),("NT","Q"),("NT","SA"),("Q","SA"),("Q","NSW"),
("NSW","SA"),("NSW","V"),("V","SA")]
G.add_edges_from(edges);

print(G.nodes(data=True))
assegnamento=backtrackingSearch(G)
colors = [color_map[assegnamento[node]] for node in G]

nx.draw(G, node_color=colors)
ax = plt.gca()
ax.collections[0].set_edgecolor("#ffffff")
plt.show()
