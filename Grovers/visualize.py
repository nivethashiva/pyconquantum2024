import numpy as np
import matplotlib.pyplot as plt

# Example data for performance analysis
classical_steps = [4, 16, 64, 256, 1024]
grover_steps = [2, 4, 8, 16, 32]
network_size = [4, 16, 64, 256, 1024]

plt.figure(figsize=(10, 6))
plt.plot(network_size, classical_steps, label='Classical Search (O(N))', marker='o')
plt.plot(network_size, grover_steps, label="Grover's Search (O(√N))", marker='x')
plt.xlabel('Network Size (Number of States)')
plt.ylabel('Number of Steps')
plt.title('Performance Comparison: Classical vs. Quantum Grover Search')
plt.legend()
plt.grid(True)
plt.show()