import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from qiskit import transpile
from qiskit_aer import Aer 
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler

# Step 1: Define the graph problem (Max-Cut)
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])

# Step 2: Create the cost operator using Qiskit's native approach
def create_cost_operator(graph):
    n = len(graph.nodes)
    pauli_list = []
    for i, j in graph.edges:
        z_pauli = ['I'] * n
        z_pauli[i] = 'Z'
        z_pauli[j] = 'Z'
        pauli_list.append((-0.5, SparsePauliOp(Pauli(''.join(z_pauli)))))
    return sum(coeff * pauli for coeff, pauli in pauli_list)

cost_operator = create_cost_operator(G)

# Step 3: Setup QAOA with an optimizer
sampler = Sampler()
optimizer = COBYLA(maxiter=200)
qaoa = QAOA(optimizer=optimizer, reps=1, sampler=sampler)

# Step 4: Run the QAOA algorithm
result = qaoa.compute_minimum_eigenvalue(cost_operator)
optimal_params = result.optimal_point

# Analyze the results
optimal_circuit = qaoa.ansatz.bind_parameters(optimal_params)
qc = transpile(optimal_circuit, backend=Aer.get_backend('aer_simulator'))
job = Aer.get_backend('aer_simulator').run(qc)
result = job.result()
counts = result.get_counts()

# Step 5: Displaying the results
most_likely_string = max(counts, key=counts.get)
max_cut_value = sum(1 for i, j in G.edges if most_likely_string[i] != most_likely_string[j])

print(f"Optimal bitstring: {most_likely_string}")
print(f"Max-Cut value: {max_cut_value}")

# Step 6: Visualization
color_map = ['lightgreen' if most_likely_string[i] == '1' else 'lightblue' for i in G.nodes]
pos = nx.spring_layout(G)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color=color_map, edge_color='gray', node_size=1000, font_size=20)
plt.title('Graph Cut by QAOA')
plt.show()