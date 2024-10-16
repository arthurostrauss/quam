from abc import ABC, abstractmethod
from collections import defaultdict

from quam.core import quam_dataclass, QuamComponent
from .gate_implementation import GateImplementation
from ..qubit_pair import QubitPair
from ..qubit import Qubit
from typing import Dict, Union, Tuple, Sequence
import numpy as np


@dataclass
class Gate(ABC):
    """
    Base class for logical native gates in QuAM.
    This class is meant to be subclassed by specific gates that are directly applicable on the hardware.
    It contains a dictionary of implementations that are specific to the hardware, indicating which qubits
    can be used to execute the gate.
    """
    unitary: np.ndarray = None

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def get_implementation(self, quantum_obj: QuantumObject) -> Optional[GateImplementation]:
        if self.name in quantum_obj.implementations:
            implementation = quantum_obj.implementations[self.name]
            if implementation.gate is self:
                return implementation

        implementations = [impl for impl in quantum_obj.implementations.values() if impl.gate is self]
        if len(implementations) != 1:
            return None
        return implementations[0]
    
    def get_implementations(self) -> Mapping[QuantumObject, GateImplementation]:
        quantum_objects = Quam.get_components(type=QuantumObject)
        gate_implementations = {q_obj: self.get_implementation(q_obj) if self.get_implementation(q_obj) is not None}
        return gate_implementations
        
    def __call__(self, quantum_obj: QuantumObject, *args, **kwargs):
        """
        Execute the gate on the specified qubits
        Args:
            qargs: Qubit(s) on which to execute the gate
            *args: Should be defined as logical gate parameters (e.g. rotation angles)
            **kwargs: Should be defined as physical gate parameters, specific to the pulse level implementation
                      (e.g. pulse amplitudes, additional phases, tweaked durations, etc.)

        Returns:

        """
        if isinstance(qargs, (Qubit, QubitPair)):
            qargs = qargs.id
        if isinstance(qargs, int):
            qargs = (qargs,)
        if not isinstance(qargs, tuple):
            qargs = tuple(qargs)

        if qargs not in self.implementations:
            raise ValueError(f"Gate {self.name} cannot be executed on qubits {qargs}")
        self.implementations[qargs].execute(*args, **kwargs)


# @quam_dataclass
# class Gate(QuamComponent, ABC):
#     """
#     Base class for logical native gates in QuAM.
#     This class is meant to be subclassed by specific gates that are directly applicable on the hardware.
#     It contains a dictionary of implementations that are specific to the hardware, indicating which qubits
#     can be used to execute the gate.
#     """
#     name: str
#     unitary: np.ndarray = None

#     def get_implementation(self, quantum_obj: QuantumObject) -> Optional[GateImplementation]:
#         if self.name in quantum_obj.implementations:
#             implementation = quantum_obj.implementations[self.name]
#             if implementation.gate is self:
#                 return implementation

#         implementations = [impl for impl in quantum_obj.implementations.values() if impl.gate is self]
#         if len(implementations) != 1:
#             return None
#         return implementations[0]
    
#     def get_implementations(self) -> Mapping[QuantumObject, GateImplementation]:
#         quantum_objects = Quam.get_components(type=QuantumObject)
#         gate_implementations = {q_obj: self.get_implementation(q_obj) if self.get_implementation(q_obj) is not None}
#         return gate_implementations
        
#     def __call__(self, quantum_obj: QuantumObject, *args, **kwargs):
#         """
#         Execute the gate on the specified qubits
#         Args:
#             qargs: Qubit(s) on which to execute the gate
#             *args: Should be defined as logical gate parameters (e.g. rotation angles)
#             **kwargs: Should be defined as physical gate parameters, specific to the pulse level implementation
#                       (e.g. pulse amplitudes, additional phases, tweaked durations, etc.)

#         Returns:

#         """
#         if isinstance(qargs, (Qubit, QubitPair)):
#             qargs = qargs.id
#         if isinstance(qargs, int):
#             qargs = (qargs,)
#         if not isinstance(qargs, tuple):
#             qargs = tuple(qargs)

#         if qargs not in self.implementations:
#             raise ValueError(f"Gate {self.name} cannot be executed on qubits {qargs}")
#         self.implementations[qargs].execute(*args, **kwargs)




X(q0)
Rx(q0, angle=phi_angle)
Rx(q0, phi_angle)

CZ(q0 @ q1)


q1.implementations["CZ"] = CZGateImplementation(...)

q1.implementations["CZ_fast"] = CZGateImplementation(...)
q1.implementations["CZ_slow"] = CZGateImplementation(...)
q1.implementations["CZ"] = "#./CZ_fast"