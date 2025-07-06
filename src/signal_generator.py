from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable


@dataclass
class SignalConfig:
    type: str = "step"  # step, ramp, sine, random
    amplitude: float = 1.0
    frequency: float = 1.0
    offset: float = 0.0


class SignalGenerator:
    """Generate simple test signals for injection."""

    def __init__(self, cfg: SignalConfig):
        self.cfg = cfg
        self._func: Callable[[float], float] = self._build_func(cfg)

    def _build_func(self, cfg: SignalConfig) -> Callable[[float], float]:
        if cfg.type == "step":
            return lambda t: cfg.offset + cfg.amplitude
        if cfg.type == "ramp":
            return lambda t: cfg.offset + cfg.amplitude * t
        if cfg.type == "sine":
            return lambda t: cfg.offset + cfg.amplitude * math.sin(2 * math.pi * cfg.frequency * t)
        if cfg.type == "random":
            return lambda t: cfg.offset + cfg.amplitude * (2 * random.random() - 1)
        return lambda t: cfg.offset

    def value(self, t: float) -> float:
        return self._func(t)
