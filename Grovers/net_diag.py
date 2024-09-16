import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Define the Network Topology
# Create a graph with 4 nodes
G = nx.Graph()

# Add nodes
G.add_node('A')
G.add_node('B')
G.add_node('C')
G.add_node('D')

# Add edges with weights representing the distance or cost
edges = [('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 2), ('C', 'D', 1), ('B', 'D', 3)]
G.add_weighted_edges_from(edges)

# Step 2: Draw the Network
pos = nx.spring_layout(G)  # Position nodes using a force-directed algorithm

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1500)

# Draw edges
nx.draw_networkx_edges(G, pos, edgelist=edges, width=2)

# Draw edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Draw node labels
nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

# Step 3: Highlight the Optimal Path (For example, let's assume Grover's Search found A -> C -> D as optimal)
optimal_path = [('A', 'C'), ('C', 'D')]
nx.draw_networkx_edges(G, pos, edgelist=optimal_path, width=4, edge_color='r')

# Display the graph
plt.title('Network Topology with Optimal Path Highlighted')
plt.show()