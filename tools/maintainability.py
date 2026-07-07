import ast
from collections import Counter


LONG_LINE_LIMIT = 120
LONG_FUNCTION_LINES = 40
TOO_MANY_PARAMS = 5
DUPLICATE_MIN_LENGTH = 30


def _finding(title, severity, line, reason, impact, recommendation):
    return {
        "title": title,
        "category": "Maintainability",
        "severity": severity,
        "location": {"line": line},
        "reason": reason,
        "impact": impact,
        "recommendation": recommendation,
    }


def analyze_maintainability(code: str) -> dict:
    findings = []
    lines = code.splitlines()

    # long lines & TODOs
    for i, line in enumerate(lines, start=1):
        if len(line) > LONG_LINE_LIMIT:
            findings.append(_finding(
                "Line exceeds recommended length",
                "low", i,
                f"Line {i} is {len(line)} characters long (limit {LONG_LINE_LIMIT}).",
                "Long lines are harder to read and to review side-by-side.",
                f"Wrap the expression to keep lines under {LONG_LINE_LIMIT} characters.",
            ))
        stripped = line.strip()
        if "TODO" in stripped or "FIXME" in stripped:
            findings.append(_finding(
                "Unresolved TODO/FIXME",
                "low", i,
                f"Line {i} contains a TODO or FIXME marker.",
                "Unresolved markers indicate incomplete work that may ship to production.",
                "Track the item in an issue tracker and remove the marker once addressed.",
            ))

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"docstring_coverage_pct": None, "findings": findings}

    total_functions = 0
    functions_with_docstring = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            total_functions += 1
            end_line = getattr(node, "end_lineno", node.lineno)
            func_len = end_line - node.lineno + 1

            if func_len > LONG_FUNCTION_LINES:
                findings.append(_finding(
                    f"Long function: {node.name}()",
                    "medium", node.lineno,
                    f"{node.name}() spans {func_len} lines (soft limit {LONG_FUNCTION_LINES}).",
                    "Long functions are harder to test and reason about.",
                    "Extract logical sections into helper functions.",
                ))

            param_count = len(node.args.args) + len(node.args.kwonlyargs)
            if param_count > TOO_MANY_PARAMS:
                findings.append(_finding(
                    f"Too many parameters in {node.name}()",
                    "medium", node.lineno,
                    f"{node.name}() takes {param_count} parameters (soft limit {TOO_MANY_PARAMS}).",
                    "Long parameter lists are hard to read and easy to call incorrectly.",
                    "Group related parameters into a dataclass or dict.",
                ))

            if ast.get_docstring(node):
                functions_with_docstring += 1
            else:
                findings.append(_finding(
                    f"Missing docstring in {node.name}()",
                    "low", node.lineno,
                    f"{node.name}() has no docstring.",
                    "Undocumented functions are harder for new contributors to use safely.",
                    "Add a short docstring explaining purpose, inputs, and return value.",
                ))

    docstring_coverage = (
        round((functions_with_docstring / total_functions) * 100, 1)
        if total_functions else None
    )

    # unused imports (module-level, best-effort)
    imported = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.append((alias.asname or alias.name.split(".")[0], node.lineno))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported.append((alias.asname or alias.name, node.lineno))

    body_text = "\n".join(
        line for line in lines
        if not (line.strip().startswith("import ") or line.strip().startswith("from "))
    )
    for name, lineno in imported:
        if name == "*":
            continue
        if name not in body_text:
            findings.append(_finding(
                f"Unused import: {name}",
                "low", lineno,
                f"'{name}' is imported but not referenced.",
                "Unused imports add noise and can hide dependency intent.",
                "Remove the import if it is genuinely unused.",
            ))

    # duplicate lines (very simple heuristic)
    normalized = [line.strip() for line in lines]
    counter = Counter(l for l in normalized if len(l) >= DUPLICATE_MIN_LENGTH)
    for line_text, count in counter.items():
        if count >= 3:
            first_line = normalized.index(line_text) + 1
            snippet = line_text if len(line_text) <= 60 else line_text[:57] + "..."
            findings.append(_finding(
                "Repeated line detected",
                "low", first_line,
                f"The line '{snippet}' appears {count} times.",
                "Repeated logic is a common source of bugs when only one copy gets updated.",
                "Extract the repeated logic into a shared helper.",
            ))

    return {
        "docstring_coverage_pct": docstring_coverage,
        "findings": findings,
    }