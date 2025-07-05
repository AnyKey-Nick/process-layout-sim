from __future__ import annotations

from collections import deque
from typing import Deque


def classify_stability(samples: list[float]) -> str:
    """Classify stability based on recent samples."""
    if len(samples) < 5:
        return "unknown"
    diff = samples[-1] - samples[0]
    if abs(diff) < 1e-3:
        return "stable"
    if diff > 0:
        return "increasing"
    return "decreasing"


class StabilityTracker:
    """Tracks a history of values and classifies behavior."""

    def __init__(self, window: int = 50):
        self.window = window
        self.data: Deque[float] = deque(maxlen=window)

    def add(self, value: float) -> None:
        self.data.append(value)

    def status(self) -> str:
        return classify_stability(list(self.data))
