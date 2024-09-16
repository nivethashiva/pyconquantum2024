import networkx as nx
import matplotlib.pyplot as plt

# Create a sample data center network graph
G = nx.Graph()

# Add nodes (servers)
G.add_nodes_from(range(6))

# Add edges (network connections) with weights representing latency
edges = [
    (0, 1, 2),
    (0, 2, 9),
    (1, 2, 3),
    (1, 3, 1),
    (2, 3, 5),
    (2, 4, 7),
    (3, 4, 4),
    (3, 5, 8),
    (4, 5, 6)
]
G.add_weighted_edges_from(edges)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()