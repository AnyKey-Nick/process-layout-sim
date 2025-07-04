from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class PIDConfig:
    Kp: float = 0.0
    Ki: float = 0.0
    Kd: float = 0.0
    setpoint: float = 0.0
    output_limits: Tuple[float, float] = (float('-inf'), float('inf'))


class PIDController:
    def __init__(self, cfg: PIDConfig):
        self.cfg = cfg
        self.integral = 0.0
        self.prev_error: Optional[float] = None

    def reset(self) -> None:
        self.integral = 0.0
        self.prev_error = None

    def compute(self, measurement: float, dt: float) -> float:
        error = self.cfg.setpoint - measurement
        if self.prev_error is None:
            self.prev_error = error
        self.integral += error * dt
        # anti-windup
        low, high = self.cfg.output_limits
        if self.integral * self.cfg.Ki > high:
            self.integral = high / self.cfg.Ki if self.cfg.Ki != 0 else self.integral
        elif self.integral * self.cfg.Ki < low:
            self.integral = low / self.cfg.Ki if self.cfg.Ki != 0 else self.integral

        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        output = (
            self.cfg.Kp * error
            + self.cfg.Ki * self.integral
            + self.cfg.Kd * derivative
        )
        output = max(low, min(high, output))
        self.prev_error = error
        return output
