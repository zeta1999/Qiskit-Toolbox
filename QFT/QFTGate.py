from qiskit.circuit import Gate
from qiskit.extensions.standard.x import CnotGate
from qiskit.extensions.standard.h import HGate
from qiskit.extensions.standard.u1 import Cu1Gate
from qiskit import QuantumRegister
from math import pi


class DoSwapsGate(Gate):
    """Do Swaps gate."""
    
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        super().__init__(name=f"Do Swaps", num_qubits=num_qubits, params=[])
        
    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        for i in range(self.num_qubits // 2):
            self.definition.append((CnotGate(), [q[i], q[self.num_qubits - i - 1]], []))
            self.definition.append((CnotGate(), [q[self.num_qubits - i - 1], q[i]], []))
            self.definition.append((CnotGate(), [q[i], q[self.num_qubits - i - 1]], []))


class QFTGate(Gate):
    """Quantum Fourier Transform gate."""
    
    def __init__(self, num_qubits, bool_swaps=True):
        self.num_qubits = num_qubits
        super().__init__(name=f"QFT", num_qubits=num_qubits, params=[bool_swaps])
        
    def _define(self):
        self.definition = []
        q = QuantumRegister(self.num_qubits)
        for i in range(self.num_qubits):
            self.definition.append((HGate(), [q[i]], []))
            for distance in range(self.num_qubits - i - 1):
                distance = distance + 1
                self.definition.append((Cu1Gate(pi / 2**distance), [q[distance + i], q[i]], []))
        if self.params[0]:
            self.definition.append((DoSwapsGate(self.num_qubits), q, []))