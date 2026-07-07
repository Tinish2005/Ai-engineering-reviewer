from .metrics import analyze_metrics
from .complexity import analyze_complexity
from .security import check_security
from .maintainability import analyze_maintainability
from .rule_engine import check_company_rules, load_rules

try:
    from .smells import detect_smells
except ImportError:
    def detect_smells(code):
        return []

__all__ = [
    "analyze_metrics",
    "analyze_complexity",
    "check_security",
    "analyze_maintainability",
    "check_company_rules",
    "load_rules",
    "detect_smells",
]
