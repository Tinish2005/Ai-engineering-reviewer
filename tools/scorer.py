def _clamp(value, lo=0, hi=100):
    return max(lo, min(hi, value))


def _security_score(security_findings):
    """
    Start at 100. Subtract per finding by severity.
    Critical: -25, High: -15, Medium: -8, Low: -3.
    """
    weights = {"critical": 25, "high": 15, "medium": 8, "low": 3, "info": 1}
    score = 100
    for f in security_findings:
        sev = f.get("severity", "info")
        score -= weights.get(sev, 5)
    return _clamp(score)


def _complexity_score(complexity):
    """
    Score based on max cyclomatic and max cognitive.
    Full marks below thresholds; steep drop above them.
    """
    max_cyc = complexity.get("cyclomatic", {}).get("max", 0)
    max_cog = complexity.get("cognitive", {}).get("max", 0)

    if max_cyc <= 5:
        cyc_score = 100
    elif max_cyc <= 10:
        cyc_score = 100 - (max_cyc - 5) * 6
    else:
        cyc_score = max(0, 70 - (max_cyc - 10) * 5)

    if max_cog <= 8:
        cog_score = 100
    elif max_cog <= 15:
        cog_score = 100 - (max_cog - 8) * 5
    else:
        cog_score = max(0, 65 - (max_cog - 15) * 4)

    return _clamp(round((cyc_score + cog_score) / 2))


def _maintainability_score(maintainability):
    """
    Base 100. Subtract based on finding severity, then adjust by docstring coverage.
    """
    findings = maintainability.get("findings", [])
    weights = {"critical": 15, "high": 10, "medium": 5, "low": 2, "info": 1}
    score = 100
    for f in findings:
        sev = f.get("severity", "low")
        score -= weights.get(sev, 2)

    coverage = maintainability.get("docstring_coverage_pct")
    if coverage is not None:
        if coverage < 30:
            score -= 10
        elif coverage < 60:
            score -= 5

    return _clamp(score)


def _documentation_score(maintainability, metrics):
    """
    Based on docstring coverage and comment ratio.
    """
    coverage = maintainability.get("docstring_coverage_pct")
    comment_ratio = metrics.get("comment_ratio_pct", 0)

    if coverage is None:
        cov_score = 50
    else:
        cov_score = _clamp(coverage)

    if comment_ratio >= 15:
        com_score = 100
    elif comment_ratio >= 5:
        com_score = 60 + (comment_ratio - 5) * 4
    else:
        com_score = _clamp(comment_ratio * 12)

    return _clamp(round((cov_score * 0.7) + (com_score * 0.3)))


def _rules_score(rule_check):
    """
    If rules were checked, score is % of rules passed.
    If no rules configured, return None (excluded from overall).
    """
    total = rule_check.get("rules_checked", 0)
    if total == 0:
        return None
    passed = rule_check.get("rules_passed", 0)
    return _clamp(round((passed / total) * 100))


def _verdict(score):
    if score >= 90:
        return "excellent"
    if score >= 75:
        return "good"
    if score >= 60:
        return "acceptable"
    if score >= 40:
        return "needs work"
    return "critical"


def compute_engineering_score(review_data, rule_check=None):
    """
    Compute per-category subscores and a weighted overall score.

    Weights (when rule check is present):
      Security: 30%, Complexity: 20%, Maintainability: 20%,
      Documentation: 10%, Company Rules: 20%.

    When no rules configured, rule weight is redistributed proportionally.
    """
    metrics = review_data.get("metrics", {})
    complexity = review_data.get("complexity", {})
    security_findings = review_data.get("security", [])
    maintainability = review_data.get("maintainability", {})

    sec = _security_score(security_findings)
    cpx = _complexity_score(complexity)
    mnt = _maintainability_score(maintainability)
    doc = _documentation_score(maintainability, metrics)
    rul = _rules_score(rule_check) if rule_check is not None else None

    if rul is None:
        weights = {"security": 0.35, "complexity": 0.25, "maintainability": 0.25, "documentation": 0.15}
        overall = round(
            sec * weights["security"]
            + cpx * weights["complexity"]
            + mnt * weights["maintainability"]
            + doc * weights["documentation"]
        )
    else:
        weights = {
            "security": 0.30,
            "complexity": 0.20,
            "maintainability": 0.20,
            "documentation": 0.10,
            "rules": 0.20,
        }
        overall = round(
            sec * weights["security"]
            + cpx * weights["complexity"]
            + mnt * weights["maintainability"]
            + doc * weights["documentation"]
            + rul * weights["rules"]
        )

    categories = [
        {"name": "Security", "score": sec, "weight_pct": round(weights["security"] * 100)},
        {"name": "Complexity", "score": cpx, "weight_pct": round(weights["complexity"] * 100)},
        {"name": "Maintainability", "score": mnt, "weight_pct": round(weights["maintainability"] * 100)},
        {"name": "Documentation", "score": doc, "weight_pct": round(weights["documentation"] * 100)},
    ]
    if rul is not None:
        categories.append({"name": "Company Rules", "score": rul, "weight_pct": round(weights["rules"] * 100)})

    return {
        "overall": _clamp(overall),
        "verdict": _verdict(overall),
        "categories": categories,
    }