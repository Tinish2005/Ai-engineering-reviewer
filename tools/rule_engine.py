import ast
import os
import yaml


DEFAULT_RULES = {
    "max_function_length": 40,
    "max_cyclomatic_complexity": 10,
    "max_cognitive_complexity": 15,
    "max_parameters": 5,
    "max_line_length": 120,
    "forbidden_calls": ["eval", "exec"],
    "forbidden_imports": [],
    "docstrings_required": False,
    "min_docstring_coverage_pct": 0,
}


def load_rules(path=None):
    if path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(project_root, "rules.yaml")

    if not os.path.exists(path):
        return dict(DEFAULT_RULES)

    try:
        with open(path, "r", encoding="utf-8") as f:
            user_rules = yaml.safe_load(f) or {}
    except Exception:
        return dict(DEFAULT_RULES)

    merged = dict(DEFAULT_RULES)
    merged.update(user_rules)
    return merged


def _finding(title, severity, line, reason, impact, recommendation):
    return {
        "title": title,
        "category": "CompanyRule",
        "severity": severity,
        "location": {"line": line},
        "reason": reason,
        "impact": impact,
        "recommendation": recommendation,
    }


def _rule_max_function_length(code, threshold):
    findings = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end_line = getattr(node, "end_lineno", node.lineno)
            func_len = end_line - node.lineno + 1
            if func_len > threshold:
                findings.append(_finding(
                    node.name + "() exceeds max function length",
                    "medium",
                    node.lineno,
                    node.name + "() is " + str(func_len) + " lines (company limit: " + str(threshold) + ").",
                    "Long functions violate the company's maintainability standard.",
                    "Split " + node.name + "() into smaller functions of at most " + str(threshold) + " lines.",
                ))
    return findings


def _rule_max_cyclomatic(review_data, threshold):
    findings = []
    per_func = review_data.get("complexity", {}).get("cyclomatic", {}).get("per_function", [])
    for fn in per_func:
        if fn.get("value", 0) > threshold:
            findings.append(_finding(
                fn["name"] + "() exceeds max cyclomatic complexity",
                "high",
                fn["line"],
                fn["name"] + "() has cyclomatic complexity " + str(fn["value"]) + " (company limit: " + str(threshold) + ").",
                "High cyclomatic complexity violates the company's simplicity standard.",
                "Reduce branching in " + fn["name"] + "() to bring it under " + str(threshold) + ".",
            ))
    return findings


def _rule_max_cognitive(review_data, threshold):
    findings = []
    per_func = review_data.get("complexity", {}).get("cognitive", {}).get("per_function", [])
    for fn in per_func:
        if fn.get("value", 0) > threshold:
            findings.append(_finding(
                fn["name"] + "() exceeds max cognitive complexity",
                "high",
                fn["line"],
                fn["name"] + "() has cognitive complexity " + str(fn["value"]) + " (company limit: " + str(threshold) + ").",
                "High cognitive complexity violates the company's readability standard.",
                "Flatten nesting in " + fn["name"] + "() to bring cognitive score under " + str(threshold) + ".",
            ))
    return findings


def _rule_max_parameters(code, threshold):
    findings = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            param_count = len(node.args.args) + len(node.args.kwonlyargs)
            if param_count > threshold:
                findings.append(_finding(
                    node.name + "() exceeds max parameter count",
                    "medium",
                    node.lineno,
                    node.name + "() has " + str(param_count) + " parameters (company limit: " + str(threshold) + ").",
                    "Long parameter lists violate the company's readability standard.",
                    "Group parameters into a dataclass to bring " + node.name + "() under " + str(threshold) + " params.",
                ))
    return findings


def _rule_max_line_length(code, threshold):
    findings = []
    for i, line in enumerate(code.splitlines(), start=1):
        if len(line) > threshold:
            findings.append(_finding(
                "Line " + str(i) + " exceeds max length",
                "low",
                i,
                "Line " + str(i) + " is " + str(len(line)) + " characters (company limit: " + str(threshold) + ").",
                "Long lines violate the company's readability standard.",
                "Wrap the expression to keep the line under " + str(threshold) + " characters.",
            ))
    return findings


def _rule_forbidden_calls(code, forbidden):
    findings = []
    for i, line in enumerate(code.splitlines(), start=1):
        for call in forbidden:
            if not isinstance(call, str):
                continue
            if call + "(" in line:
                findings.append(_finding(
                    "Forbidden call: " + call + "()",
                    "high",
                    i,
                    call + "() is on the company's forbidden call list.",
                    "The company prohibits this call for security or reliability reasons.",
                    "Remove all calls to " + call + "() and use an approved alternative.",
                ))
    return findings


def _rule_forbidden_imports(code, forbidden):
    findings = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split(".")[0]
                if name in forbidden:
                    findings.append(_finding(
                        "Forbidden import: " + name,
                        "high",
                        node.lineno,
                        "'" + name + "' is on the company's forbidden import list.",
                        "The company prohibits this import for security or policy reasons.",
                        "Remove the import of '" + name + "' and use an approved alternative.",
                    ))
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in forbidden:
                findings.append(_finding(
                    "Forbidden import: " + node.module,
                    "high",
                    node.lineno,
                    "'" + node.module + "' is on the company's forbidden import list.",
                    "The company prohibits this import for security or policy reasons.",
                    "Remove the import of '" + node.module + "' and use an approved alternative.",
                ))
    return findings


def _rule_docstrings_required(code):
    findings = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not ast.get_docstring(node):
                findings.append(_finding(
                    "Missing required docstring in " + node.name + "()",
                    "medium",
                    node.lineno,
                    node.name + "() has no docstring.",
                    "The company requires docstrings on all functions.",
                    "Add a docstring to " + node.name + "() describing its purpose.",
                ))
    return findings


def _rule_min_docstring_coverage(review_data, threshold):
    findings = []
    coverage = review_data.get("maintainability", {}).get("docstring_coverage_pct")
    if coverage is not None and coverage < threshold:
        findings.append(_finding(
            "Docstring coverage below company minimum",
            "medium",
            0,
            "Docstring coverage is " + str(coverage) + "% (company minimum: " + str(threshold) + "%).",
            "Insufficient documentation violates the company's coverage standard.",
            "Add docstrings to more functions to reach at least " + str(threshold) + "% coverage.",
        ))
    return findings


def check_company_rules(code, review_data, rules=None):
    if rules is None:
        rules = load_rules()

    results = []

    v = rules.get("max_function_length")
    if isinstance(v, int) and v > 0:
        f = _rule_max_function_length(code, v)
        results.append({"rule": "max_function_length", "threshold": v, "status": "pass" if not f else "fail", "findings": f})

    v = rules.get("max_cyclomatic_complexity")
    if isinstance(v, int) and v > 0:
        f = _rule_max_cyclomatic(review_data, v)
        results.append({"rule": "max_cyclomatic_complexity", "threshold": v, "status": "pass" if not f else "fail", "findings": f})

    v = rules.get("max_cognitive_complexity")
    if isinstance(v, int) and v > 0:
        f = _rule_max_cognitive(review_data, v)
        results.append({"rule": "max_cognitive_complexity", "threshold": v, "status": "pass" if not f else "fail", "findings": f})

    v = rules.get("max_parameters")
    if isinstance(v, int) and v > 0:
        f = _rule_max_parameters(code, v)
        results.append({"rule": "max_parameters", "threshold": v, "status": "pass" if not f else "fail", "findings": f})

    v = rules.get("max_line_length")
    if isinstance(v, int) and v > 0:
        f = _rule_max_line_length(code, v)
        results.append({"rule": "max_line_length", "threshold": v, "status": "pass" if not f else "fail", "findings": f})

    v = rules.get("forbidden_calls", [])
    if isinstance(v, list) and v:
        f = _rule_forbidden_calls(code, v)
        results.append({"rule": "forbidden_calls", "threshold": ", ".join(str(x) for x in v), "status": "pass" if not f else "fail", "findings": f})

    v = rules.get("forbidden_imports", [])
    if isinstance(v, list) and v:
        f = _rule_forbidden_imports(code, v)
        results.append({"rule": "forbidden_imports", "threshold": ", ".join(str(x) for x in v), "status": "pass" if not f else "fail", "findings": f})

    if rules.get("docstrings_required") is True:
        f = _rule_docstrings_required(code)
        results.append({"rule": "docstrings_required", "threshold": "true", "status": "pass" if not f else "fail", "findings": f})

    v = rules.get("min_docstring_coverage_pct")
    if isinstance(v, (int, float)) and v > 0:
        f = _rule_min_docstring_coverage(review_data, v)
        results.append({"rule": "min_docstring_coverage_pct", "threshold": v, "status": "pass" if not f else "fail", "findings": f})

    passed = sum(1 for r in results if r["status"] == "pass")
    failed = sum(1 for r in results if r["status"] == "fail")

    return {
        "rules_checked": len(results),
        "rules_passed": passed,
        "rules_failed": failed,
        "results": results,
    }
