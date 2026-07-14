from tools import (
    analyze_metrics,
    analyze_complexity,
    check_security,
    analyze_maintainability,
    check_company_rules,
    compute_engineering_score,
    detect_language,
    language_label,
)

from ai_layer import generate_review_reasoning
from tools.history import save_review


def run_review(code: str) -> dict:

    language = detect_language(code)

    metrics = analyze_metrics(
        code,
        language
    )

    complexity = analyze_complexity(
        code,
        language
    )

    security_findings = check_security(
        code,
        language
    )

    maintainability = analyze_maintainability(
        code,
        language
    )

    review_data = {
        "metrics": metrics,
        "complexity": complexity,
        "security": security_findings,
        "maintainability": maintainability,
        "language": language,
    }

    rule_check = check_company_rules(
        code,
        review_data
    )

    score = compute_engineering_score(
        review_data,
        rule_check
    )

    reasoning = generate_review_reasoning(
        review_data
    )

    review_result = {
        "type": "review",
        "language": language,
        "language_label": language_label(language),
        "components": [
            {
                "type": "score_card",
                "title": "Engineering Score",
                "overall": score["overall"],
                "verdict": score["verdict"],
                "categories": score["categories"],
                "language": language_label(language),
            },
            {
                "type": "metric_card",
                "title": "Code Metrics",
                "data": metrics,
            },
            {
                "type": "complexity_card",
                "title": "Complexity",
                "cyclomatic_max": complexity["cyclomatic"]["max"],
                "cognitive_max": complexity["cognitive"]["max"],
                "verdict": complexity["verdict"],
                "per_function_cyclomatic":
                    complexity["cyclomatic"]["per_function"],
                "per_function_cognitive":
                    complexity["cognitive"]["per_function"],
                "findings":
                    complexity.get("findings", []),
                "note":
                    complexity.get("note", ""),
            },
            {
                "type": "finding_list",
                "title": "Security",
                "findings": security_findings,
            },
            {
                "type": "finding_list",
                "title": "Maintainability",
                "findings":
                    maintainability["findings"],
                "docstring_coverage_pct":
                    maintainability.get(
                        "docstring_coverage_pct"
                    ),
            },
            {
                "type": "rule_check_card",
                "title": "Company Rules",
                "rules_checked":
                    rule_check["rules_checked"],
                "rules_passed":
                    rule_check["rules_passed"],
                "rules_failed":
                    rule_check["rules_failed"],
                "results":
                    rule_check["results"],
            },
            {
                "type": "ai_summary",
                "title": "AI Reasoning",
                "summary":
                    reasoning.get(
                        "summary",
                        ""
                    ),
                "priority_issues":
                    reasoning.get(
                        "priority_issues",
                        []
                    ),
                "suggestions":
                    reasoning.get(
                        "suggestions",
                        []
                    ),
            },
        ],
    }

    save_review(
        language=language_label(language),
        score=score["overall"],
        code=code,
        result=review_result,
    )

    return review_result