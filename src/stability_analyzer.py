from __future__ import annotations

from collections import deque


class StabilityAnalyzer:
    """Simple heuristic-based stability analyzer."""

    def __init__(self, window: int = 100):
        self.window = window
        self.values: deque[float] = deque(maxlen=window)

    def update(self, value: float) -> str:
        self.values.append(value)
        return self.classify()

    def classify(self) -> str:
        if len(self.values) < 2:
            return "unknown"
        span = max(self.values) - min(self.values)
        if span < 0.05:
            return "stable"
        if span > 5:
            return "unstable"
        return "marginal"
