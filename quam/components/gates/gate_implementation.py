from abc import ABC, abstractmethod
from typing import Dict
from dataclasses import field
from copy import copy

from quam.components.pulses import Pulse
from quam.core import quam_dataclass, QuamComponent
from quam.utils import string_reference as str_ref

@quam_dataclass
class GateImplementation(QuamComponent, ABC):
    """
    Base class for gate implementations
    """
    gate_name: str

    @property
    def qubits(self):
        from ..quantum_object import QuantumObject

        if isinstance(self.parent, QuantumObject):
            return self.parent
        elif hasattr(self.parent, "parent") and isinstance(self.parent.parent, QuantumObject):
            return self.parent.parent

        else:
            raise AttributeError(
                "GateImplementation is not attached to a qubit or qubit pair. GateImplementation: {self}"
            )


    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the gate implementation
        Args:
            *args: Should be defined as logical gate parameters (e.g. rotation angles)
            **kwargs: Should be defined as physical gate parameters, specific to the pulse level implementation
                      (e.g. pulse amplitudes, additional phases, tweaked durations, etc.)

        Returns:

        """
        pass

    def __call__(self, *args, **kwargs):
        self.execute(*args, **kwargs)



X_gate_implementation.gate = X_gate.get_reference()  # #/gates/X
X_gate_implementation.gate  # X_gate