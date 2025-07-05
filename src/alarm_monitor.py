from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AlarmConfig:
    low: float | None = None
    high: float | None = None


class AlarmMonitor:
    def __init__(self, cfg: AlarmConfig | None = None):
        self.cfg = cfg or AlarmConfig()
        self.active = False

    def update(self, value: float) -> bool:
        """Return True if alarm is active."""
        low = self.cfg.low
        high = self.cfg.high
        self.active = False
        if low is not None and value < low:
            self.active = True
        if high is not None and value > high:
            self.active = True
        return self.active
