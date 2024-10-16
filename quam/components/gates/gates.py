from quam.components.gates.gate import Gate


class X(Gate):
    def __call__(self, quantum_obj: Qubit, *args, **kwargs):
        assert not args
        return super().__call__(quantum_obj, **kwargs)


class Y(Gate):
    def __call__(self, quantum_obj: Qubit, *args, **kwargs):
        assert not args
        return super().__call__(quantum_obj, **kwargs)


class CZ(Gate):
    def __call__(self, quantum_obj: QubitPair, *args, **kwargs):
        return super().__call__(quantum_obj, **kwargs)

