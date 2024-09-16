from qiskit_aer import Aer
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit.quantum_info import SparsePauliOp
import matplotlib.pyplot as plt
import networkx as nx
import time

# Define the network graph
graph = nx.Graph()
graph.add_weighted_edges_from([(0, 1, 1), (1, 2, 2), (2, 3, 3), (3, 0, 4), (0, 2, 5)])

# Visualize the network
nx.draw(graph, with_labels=True, node_color='lightblue', font_weight='bold')
plt.show()

# Define the problem Hamiltonian (simplified example)
qubit_op = SparsePauliOp.from_list([("ZZ", 1.0)])

# Create the QAOA instance with the required sampler
sampler = Sampler()
optimizer = COBYLA(maxiter=100)
qaoa = QAOA(optimizer=optimizer, sampler=sampler, reps=1)

# Execute the QAOA
result = qaoa.compute_minimum_eigenvalue(qubit_op)

# Display the result
print("Optimal Value:", result.eigenvalue.real)

# Classical simulation (dummy timing for comparison)
start_time_classical = time.time()
# Simulate a classical routing algorithm here (this is a placeholder)
end_time_classical = time.time()

# Quantum simulation (using QAOA)
start_time_quantum = time.time()
result = qaoa.compute_minimum_eigenvalue(qubit_op)
end_time_quantum = time.time()

# Calculate the time taken for both approaches
classical_time = end_time_classical - start_time_classical
quantum_time = end_time_quantum - start_time_quantum

# Plot the performance comparison
plt.bar(['Classical', 'Quantum'], [classical_time, quantum_time], color=['blue', 'green'])
plt.ylabel('Time Taken (s)')
plt.title('Performance Comparison: Classical vs Quantum')
plt.show()