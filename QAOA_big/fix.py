import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
from qiskit import transpile, QuantumCircuit
from qiskit_aer import Aer
from qiskit_algorithms import QAOA
from qiskit.primitives import Sampler
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms.optimizers import COBYLA
from qiskit.quantum_info import SparsePauliOp, Pauli

# Define a more complex graph
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
G = nx.Graph()
G.add_weighted_edges_from(edges)

# Visualize the graph
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()

# QAOA Parameters
problem = QuadraticProgram()

# Add binary variables
for i in range(len(G.nodes)):
    problem.binary_var(f'x{i}')

# Define the objective function as the sum of the weights on the edges
objective = {}
for i, j, w in edges:
    objective[f'x{i}'] = w
    objective[f'x{j}'] = w

# Set the objective to minimize
problem.minimize(linear=objective)

# Convert problem to QUBO
qubo = QuadraticProgramToQubo().convert(problem)

# Define the cost operator manually
op = SparsePauliOp.from_operator(qubo.to_ising()[0])

# Set up the QAOA with COBYLA optimizer
sampler = Sampler()
qaoa = QAOA(optimizer=COBYLA(), reps=200, sampler=sampler)
qaoa_optimizer = MinimumEigenOptimizer(qaoa)

# Solve the problem using QAOA
start_time_qaoa = time.time()
result_qaoa = qaoa_optimizer.solve(problem)
qaoa_time = time.time() - start_time_qaoa

# Solve using a classical method (Dijkstra’s Algorithm)
start_time_classical = time.time()
classical_result = nx.dijkstra_path(G, source=0, target=8)
classical_time = time.time() - start_time_classical

# Performance comparison
times = [classical_time, qaoa_time]
labels = ['Classical (Dijkstra)', 'Quantum (QAOA)']
colors = ['blue', 'green']

plt.figure(figsize=(8, 6))
plt.bar(labels, times, color=colors)
plt.ylabel('Time Taken (s)')
plt.title('Performance Comparison: Classical vs Quantum')
plt.show()

print(f"Classical Time: {classical_time:.4f}s")
print(f"Quantum (QAOA) Time: {qaoa_time:.4f}s")