import ast

from .language_detector import detect_language
from .lang_java import analyze_java_complexity
from .lang_c_cpp import analyze_c_complexity


_DECISION_NODES = (
    ast.If, ast.For, ast.While, ast.ExceptHandler,
    ast.BoolOp, ast.IfExp,
)


def _cyclomatic_for_function(func_node):
    count = 1
    for node in ast.walk(func_node):
        if isinstance(node, _DECISION_NODES):
            if isinstance(node, ast.BoolOp):
                count += max(0, len(node.values) - 1)
            else:
                count += 1
    return count


def _cognitive_for_function(func_node):
    score = 0

    def walk(node, depth):
        nonlocal score
        for child in ast.iter_child_nodes(node):
            if isinstance(child, _DECISION_NODES):
                score += 1 + depth
                walk(child, depth + 1)
            else:
                walk(child, depth)

    walk(func_node, 0)
    return score


def analyze_complexity(code: str, language: str = None) -> dict:
    """
    Compute complexity metrics.
    Python uses AST analysis; other languages use regex heuristics.
    """
    if language is None:
        language = detect_language(code)

    if language == "java":
        return analyze_java_complexity(code)
    if language in ("c", "cpp"):
        return analyze_c_complexity(code)

    # Python AST-based analysis
    findings = []
    functions = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            "cyclomatic": {"per_function": [], "max": 0},
            "cognitive": {"per_function": [], "max": 0},
            "verdict": "unparseable",
            "findings": [{
                "title": "Code failed to parse",
                "category": "Complexity",
                "severity": "info",
                "location": {"line": e.lineno or 0},
                "reason": f"Python could not parse the code: {e.msg}",
                "impact": "Complexity analysis is skipped when the code has syntax errors.",
                "recommendation": "Fix the syntax error and re-run the analysis.",
            }],
        }

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            cyc = _cyclomatic_for_function(node)
            cog = _cognitive_for_function(node)
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "cyclomatic": cyc,
                "cognitive": cog,
            })
            if cyc > 10:
                findings.append({
                    "title": f"High cyclomatic complexity in {node.name}()",
                    "category": "Complexity",
                    "severity": "high" if cyc > 20 else "medium",
                    "location": {"line": node.lineno},
                    "reason": f"{node.name}() has cyclomatic complexity {cyc}.",
                    "impact": "Functions above 10 are harder to reason about and test thoroughly.",
                    "recommendation": "Extract helper functions, or split into smaller units of work.",
                })
            if cog > 15:
                findings.append({
                    "title": f"High cognitive complexity in {node.name}()",
                    "category": "Complexity",
                    "severity": "high" if cog > 25 else "medium",
                    "location": {"line": node.lineno},
                    "reason": f"{node.name}() has cognitive complexity {cog}.",
                    "impact": "Deeply nested logic is hard for humans to hold in mind while reading.",
                    "recommendation": "Flatten nesting with early returns or extract nested blocks into helpers.",
                })

    max_cyc = max((f["cyclomatic"] for f in functions), default=0)
    max_cog = max((f["cognitive"] for f in functions), default=0)

    if max_cyc <= 5 and max_cog <= 8:
        verdict = "simple"
    elif max_cyc <= 10 and max_cog <= 15:
        verdict = "moderate"
    else:
        verdict = "complex"

    return {
        "cyclomatic": {
            "per_function": [{"name": f["name"], "line": f["line"], "value": f["cyclomatic"]} for f in functions],
            "max": max_cyc,
        },
        "cognitive": {
            "per_function": [{"name": f["name"], "line": f["line"], "value": f["cognitive"]} for f in functions],
            "max": max_cog,
        },
        "verdict": verdict,
        "findings": findings,
    }