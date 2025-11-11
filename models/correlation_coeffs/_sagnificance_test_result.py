from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class SignificanceTestResult:
    """Result of correlation significance test."""
    statistic: float
    p_value: float
    is_significant: bool
    alpha: float
    test_name: str
    critical_value: Optional[float] = None
    CI: Optional[Tuple[float, float]] = None
    
    def __str__(self) -> str:
        sig = "SIGNIFICANT" if self.is_significant else "NOT SIGNIFICANT"
        return (
                f"{self.test_name}: statistic={self.statistic:.4f}, "
                f"p-value={self.p_value:.4f} -> {sig} (α={self.alpha})"
                f"Confidence interval: ({self.CI[0]:.3f}, {self.CI[1]:.3f}" if self.is_significant else "No interval available"
                )