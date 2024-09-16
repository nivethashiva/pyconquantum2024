from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Oracle for marking the desired state |11>
def grover_oracle(n_qubits):
    oracle = QuantumCircuit(n_qubits)
    oracle.cz(0, 1)  # Mark the state |11> as the "optimal path"
    oracle = oracle.to_gate()
    oracle.name = "Oracle"
    return oracle

# Grover diffuser to amplify the probability of the marked state
def diffuser(n_qubits):
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)  # multi-controlled X gate
    qc.h(n_qubits - 1)
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))
    qc = qc.to_gate()
    qc.name = "Diffuser"
    return qc

# Number of qubits
n_qubits = 10
grover_circuit = QuantumCircuit(n_qubits)

# Apply Hadamard gates to all qubits to create superposition
grover_circuit.h(range(n_qubits))

# Append the oracle and diffuser gates to the circuit
grover_circuit.append(grover_oracle(n_qubits), range(n_qubits))
grover_circuit.append(diffuser(n_qubits), range(n_qubits))

# Add measurement operations to all qubits
grover_circuit.measure_all()

# Transpile the circuit for optimization
backend = Aer.get_backend('qasm_simulator')
transpiled_circuit = transpile(grover_circuit, backend)

# Use the Qiskit Primitives Sampler to run the circuit
sampler = Sampler()
job = sampler.run(transpiled_circuit)
result = job.result()

# Extract quasi-distribution from the result
quasi_dists = result.quasi_dists[0]  # This is a list of quasi-distributions, taking the first

# Convert quasi-distribution to counts-like dictionary
counts = {f"{k:0{n_qubits}b}": v for k, v in quasi_dists.items()} # Ensure keys are in binary string format

# Print and visualize the results
print("Result from Grover's Search Algorithm:", counts)
plot_histogram(counts)
plt.show()