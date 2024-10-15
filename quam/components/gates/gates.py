from abc import ABC, abstractmethod
from collections import defaultdict

from quam.core import quam_dataclass, QuamComponent
from .gate_implementation import GateImplementation
from ..qubit_pair import QubitPair
from ..qubit import Qubit
from typing import Dict, Union, Tuple, Sequence
import numpy as np


@quam_dataclass
class Gate(QuamComponent, ABC):
    """
    Base class for logical native gates in QuAM.
    This class is meant to be subclassed by specific gates that are directly applicable on the hardware.
    It contains a dictionary of implementations that are specific to the hardware, indicating which qubits
    can be used to execute the gate.
    """
    name: str
    implementations: Dict[Union[Qubit, QubitPair, Tuple[Union[int, str]]], GateImplementation] = defaultdict(dict)
    unitary: np.ndarray = None

    def __post_init__(self) -> None:

        for imp in self.implementations.keys():
            if not isinstance(imp, (Qubit, QubitPair, Tuple)):
                raise ValueError(f"Invalid implementation key: {imp}")
            # Check that the implementation is a GateImplementation
            if not isinstance(self.implementations[imp], GateImplementation):
                raise ValueError(f"Invalid implementation: {self.implementations[imp]}")
            # Check that all keys correspond to the same number of qubits
            if isinstance(imp, Tuple):
                n_qargs = len(imp)
                if len(imp) != len(self.implementations[imp].qubits):
                    raise ValueError(f"Invalid implementation key: {imp}")




    def __call__(self, qargs: Union[Sequence[Union[int, str]], Qubit, QubitPair], *args, **kwargs):
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



