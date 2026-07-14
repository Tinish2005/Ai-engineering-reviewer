from .metrics import analyze_metrics
from .complexity import analyze_complexity
from .security import check_security
from .maintainability import analyze_maintainability
from .rule_engine import check_company_rules, load_rules
from .scorer import compute_engineering_score
from .language_detector import detect_language, language_label

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
    "compute_engineering_score",
    "detect_language",
    "language_label",
    "detect_smells",
]