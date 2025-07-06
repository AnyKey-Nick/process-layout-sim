from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class AlarmConfig:
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    hysteresis: float = 0.0
    enabled: bool = True


class AlarmMonitor:
    """Check values against limits and report alarm state."""

    def __init__(self, cfg: AlarmConfig):
        self.cfg = cfg
        self._active = False

    @property
    def active(self) -> bool:
        return self._active

    def check(self, value: float) -> bool:
        if not self.cfg.enabled:
            self._active = False
            return False
        if self._active:
            if self.cfg.minimum is not None and value > self.cfg.minimum + self.cfg.hysteresis:
                self._active = False
            elif self.cfg.maximum is not None and value < self.cfg.maximum - self.cfg.hysteresis:
                self._active = False
        else:
            if self.cfg.minimum is not None and value < self.cfg.minimum:
                self._active = True
            if self.cfg.maximum is not None and value > self.cfg.maximum:
                self._active = True
        return self._active
