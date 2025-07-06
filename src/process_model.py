from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProcessState:
    value: float
    derivative: float = 0.0


class ProcessModel:
    def __init__(self, parameters: dict, initial_value: float = 0.0):
        self.params = parameters
        self.state = ProcessState(initial_value)

    def update(self, u: float, dt: float) -> float:
        raise NotImplementedError


class FirstOrderProcess(ProcessModel):
    """Simple first order thermal process."""

    def update(self, u: float, dt: float) -> float:
        tau = self.params.get('tau', 1.0)
        ambient = self.params.get('ambient', 0.0)
        capacity = self.params.get('capacity', 1.0)
        value = self.state.value
        dTdt = -((value - ambient) / tau) + (u / capacity)
        value += dTdt * dt
        # optional process noise
        noise = self.params.get('noise_std', 0.0)
        if noise:
            import random
            value += random.gauss(0.0, noise)
        self.state.value = value
        self.state.derivative = dTdt
        return value


class SecondOrderProcess(ProcessModel):
    """Second order process with damping."""

    def __init__(self, parameters: dict, initial_value: float = 0.0):
        super().__init__(parameters, initial_value)
        self.velocity = 0.0

    def update(self, u: float, dt: float) -> float:
        wn = self.params.get('wn', 1.0)
        zeta = self.params.get('zeta', 0.7)
        gain = self.params.get('gain', 1.0)

        accel = gain * u - 2 * zeta * wn * self.velocity - (wn ** 2) * self.state.value
        self.velocity += accel * dt
        self.state.value += self.velocity * dt
        # optional process noise
        noise = self.params.get('noise_std', 0.0)
        if noise:
            import random
            self.state.value += random.gauss(0.0, noise)
        self.state.derivative = self.velocity
        return self.state.value


def create_process(model_name: str, parameters: dict, initial_value: float) -> ProcessModel:
    if model_name == 'first_order':
        return FirstOrderProcess(parameters, initial_value)
    if model_name == 'second_order':
        return SecondOrderProcess(parameters, initial_value)
    raise ValueError(f"Unknown model {model_name}")
