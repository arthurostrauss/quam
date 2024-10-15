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

    @property
    def qubits(self):
        from ..qubit import Qubit
        from ..qubit_pair import QubitPair

        if isinstance(self.parent, Qubit):
            return self.parent
        elif isinstance(self.parent, QubitPair):
            return self.parent.qubit_control, self.parent.qubit_target

        elif hasattr(self.parent, "parent") and isinstance(self.parent.parent, Qubit):
            return self.parent.parent
        elif hasattr(self.parent, "parent") and isinstance(self.parent.parent, QubitPair):
            return self.parent.parent.qubit_control, self.parent.parent.qubit_target

        else:
            raise AttributeError(
                "GateImplementation is not attached to a qubit or qubit pair. GateImplementation: {self}"
            )

    @property
    def definition(self):
        return self._definition


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



