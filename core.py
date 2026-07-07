from tools import (
    analyze_metrics,
    analyze_complexity,
    check_security,
    analyze_maintainability,
    check_company_rules,
)
from ai_layer import generate_review_reasoning


def run_review(code: str) -> dict:
    metrics = analyze_metrics(code)
    complexity = analyze_complexity(code)
    security_findings = check_security(code)
    maintainability = analyze_maintainability(code)

    review_data = {
        "metrics": metrics,
        "complexity": complexity,
        "security": security_findings,
        "maintainability": maintainability,
    }

    rule_check = check_company_rules(code, review_data)
    reasoning = generate_review_reasoning(review_data)

    return {
        "type": "review",
        "components": [
            {"type": "metric_card", "title": "Code Metrics", "data": metrics},
            {
                "type": "complexity_card",
                "title": "Complexity",
                "cyclomatic_max": complexity["cyclomatic"]["max"],
                "cognitive_max": complexity["cognitive"]["max"],
                "verdict": complexity["verdict"],
                "per_function_cyclomatic": complexity["cyclomatic"]["per_function"],
                "per_function_cognitive": complexity["cognitive"]["per_function"],
                "findings": complexity.get("findings", []),
            },
            {"type": "finding_list", "title": "Security", "findings": security_findings},
            {
                "type": "finding_list",
                "title": "Maintainability",
                "findings": maintainability["findings"],
                "docstring_coverage_pct": maintainability["docstring_coverage_pct"],
            },
            {
                "type": "rule_check_card",
                "title": "Company Rules",
                "rules_checked": rule_check["rules_checked"],
                "rules_passed": rule_check["rules_passed"],
                "rules_failed": rule_check["rules_failed"],
                "results": rule_check["results"],
            },
            {
                "type": "ai_summary",
                "title": "AI Reasoning",
                "summary": reasoning.get("summary", ""),
                "priority_issues": reasoning.get("priority_issues", []),
                "suggestions": reasoning.get("suggestions", []),
            },
        ],
    }
