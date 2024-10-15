from typing import Dict, Union
from dataclasses import field

from quam.core import quam_dataclass, QuamComponent
from quam.components.qubit import Qubit
from quam.components.gates.two_qubit_gates import TwoQubitGate


@quam_dataclass
class QubitPair(QuamComponent):
    qubit_control: Qubit
    qubit_target: Qubit
    gates: Dict[str, TwoQubitGate] = field(default_factory=dict)

    def apply(self, gate: Union[str, TwoQubitGate], *args, **kwargs):
        """
        Apply a gate to the qubit pair.

        Args:
            gate (TwoQubitGate or str): The gate to apply. Can be a gate object
                or the name of the gate to apply.
            *args: Arguments to pass to the gate's `execute` method.
            **kwargs: Keyword arguments to pass to the gate's `execute` method.
        """
        if isinstance(gate, str) and gate in self.gates:
            gate = self.gates[gate]
        elif isinstance(gate, TwoQubitGate) and gate.name in self.gates:
            gate = self.gates[gate.name]
        else:
            raise ValueError(
                f"Gate not found in qubit gates: {gate=}, {self.gates=}"
            )

        gate.execute(*args, **kwargs)

