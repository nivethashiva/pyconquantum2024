from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.primitives import Sampler
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit.quantum_info import SparsePauliOp
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import time

# Define a larger network graph
edges = [
    (0, 1, 2),
    (0, 2, 9),
    (1, 2, 3),
    (1, 3, 1),
    (2, 3, 5),
    (2, 4, 7),
    (3, 4, 4),
    (3, 5, 8),
    (4, 5, 6),
    (4, 6, 3),
    (5, 6, 2),
    (5, 7, 9),
    (6, 7, 7),
    (6, 8, 5),
    (7, 8, 4)
]

graph = nx.Graph()
graph.add_weighted_edges_from(edges)

# Visualize the network
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, node_color='lightblue', font_weight='bold', edge_color='gray')
labels = nx.get_edge_attributes(graph, 'weight')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
plt.show()

def classical_shortest_path(graph, source, target):
    return nx.dijkstra_path_length(graph, source, target, weight='weight')

# Classical performance analysis
start_time_classical = time.time()
shortest_path_classical = classical_shortest_path(graph, 0, 8)
end_time_classical = time.time()

print("Classical Shortest Path Cost:", shortest_path_classical)
print("Classical Execution Time:", end_time_classical - start_time_classical)

# Define the problem Hamiltonian (simplified example)
# For a larger graph, we'll assume a simplified Hamiltonian for demonstration purposes
n_qubits = len(graph.nodes)

# used for performing operator arithmetic for hundred of qubits 
qubit_op = SparsePauliOp.from_list([("ZZ", 1.0)])

## Create the QAOA instance with the required sampler 
# (A Sampler calculates probabilities or quasi-probabilities of bitstrings from quantum circuits)
sampler = Sampler()

# COBYLA is a numerical optimization method for constrained problems 
optimizer = COBYLA(maxiter=100)
qaoa = QAOA(optimizer=optimizer, sampler=sampler, reps=100)

# Execute the QAOA
start_time_quantum = time.time()
# the value of measurable quantity associated with the quantum function. 
# If you want to measure the time taken, you have to operate on the quantum function with the Hamiltonian operator 
result = qaoa.compute_minimum_eigenvalue(qubit_op)
end_time_quantum = time.time()

print("Quantum Optimal Value:", result.eigenvalue.real)
print("Quantum Execution Time:", end_time_quantum - start_time_quantum)

# Plot the performance comparison
times = [end_time_quantum - start_time_quantum, end_time_classical - start_time_classical]
plt.bar(['Classical (Dijkstra)', 'Quantum (QAOA)'], times, color=['blue', 'green'])
plt.ylabel('Time Taken (s)')
plt.yscale('log')
plt.title('Performance Comparison: Classical vs Quantum')
plt.show()