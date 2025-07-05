from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass
class SignalConfig:
    """Configuration for signal generation."""

    type: str = "step"  # step, ramp, sine, pulse, random
    amplitude: float = 1.0
    offset: float = 0.0
    frequency: float = 1.0
    start: float = 0.0
    end: float = float("inf")


class SignalGenerator:
    def __init__(self, cfg: SignalConfig | None = None):
        self.cfg = cfg or SignalConfig()

    def value(self, t: float) -> float:
        if t < self.cfg.start or t > self.cfg.end:
            return self.cfg.offset
        kind = self.cfg.type
        a = self.cfg.amplitude
        if kind == "step":
            return self.cfg.offset + a
        if kind == "ramp":
            return self.cfg.offset + a * (t - self.cfg.start)
        if kind == "sine":
            return self.cfg.offset + a * math.sin(2 * math.pi * self.cfg.frequency * t)
        if kind == "pulse":
            period = 1.0 / max(self.cfg.frequency, 1e-6)
            return self.cfg.offset + (a if (t - self.cfg.start) % period < period / 2 else 0)
        if kind == "random":
            return self.cfg.offset + a * (2 * random.random() - 1)
        return self.cfg.offset
