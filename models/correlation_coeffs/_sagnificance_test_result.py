from dataclasses import dataclass
from typing import Optional, Tuple, Dict

@dataclass
class SignificanceTestResult:
    """Result of correlation significance test."""
    r: float
    statistic: float
    p_value: float
    is_significant: bool
    alpha: float
    test_name: str
    critical_value: Optional[float] = None
    CI: Optional[Tuple[float, float]] = None
    extra: Optional[Dict[str, str|float]] = None
    
    def __str__(self) -> str:
        sig = "SIGNIFICANT" if self.is_significant else "NOT SIGNIFICANT"
        extra_str = ""
        if self.extra:
            extra_lines = [f"{k} = {v}" for k, v in self.extra.items()]
            extra_str = "\n".join(extra_lines) + "\n"
        ci_str = (
            f"{self.CI[0]:.3f} <= r={self.r:.3f} <= {self.CI[1]:.3f}"
            if self.CI
            else "No interval available"
        )
        return (
            f"{self.test_name} (r) = {self.r:.3f}\n"
            f"statistic={self.statistic:.4f}\n"
            f"{extra_str}"
            f"p-value={self.p_value:.4f} -> {sig} (α={self.alpha})\n"
            f"{ci_str}"
        )