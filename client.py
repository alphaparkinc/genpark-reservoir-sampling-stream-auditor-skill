"""Reservoir Sampling Stream Auditor Engine.
100% Python Standard Library.
"""

import math
import random
from typing import Dict, List, Any, Optional

class ReservoirSamplingStreamAuditor:
    """Algorithm R unbiased reservoir sampler and streaming percentile estimator."""

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.reservoir: List[Dict[str, Any]] = []
        self.total_seen = 0
        self.sum = 0.0
        self.sq_sum = 0.0
        self.min_val: Optional[float] = None
        self.max_val: Optional[float] = None

    def feed(self, value: float, item_id: Any = None):
        self.total_seen += 1
        self.sum += value
        self.sq_sum += value * value
        if self.min_val is None or value < self.min_val:
            self.min_val = value
        if self.max_val is None or value > self.max_val:
            self.max_val = value

        entry = {"value": value, "id": item_id, "index": self.total_seen}
        if len(self.reservoir) < self.capacity:
            self.reservoir.append(entry)
        else:
            j = random.randint(1, self.total_seen)
            if j <= self.capacity:
                self.reservoir[j - 1] = entry

    def get_quantiles(self, percentiles: List[float] = [0.5, 0.9, 0.95, 0.99]) -> Dict[str, float]:
        if not self.reservoir:
            return {}
        sorted_vals = sorted(e["value"] for e in self.reservoir)
        n = len(sorted_vals)
        results = {}
        for p in percentiles:
            idx = min(int(round(p * (n - 1))), n - 1)
            results[f"p{int(p*100)}"] = sorted_vals[idx]
        return results

    def get_summary(self) -> Dict[str, Any]:
        mean = (self.sum / self.total_seen) if self.total_seen > 0 else 0.0
        variance = 0.0
        if self.total_seen > 1:
            variance = (self.sq_sum - (self.sum ** 2) / self.total_seen) / (self.total_seen - 1)
        return {
            "total_seen": self.total_seen,
            "sample_size": len(self.reservoir),
            "mean": round(mean, 4),
            "stddev": round(math.sqrt(max(0, variance)), 4),
            "min": self.min_val,
            "max": self.max_val,
            "quantiles": self.get_quantiles()
        }
