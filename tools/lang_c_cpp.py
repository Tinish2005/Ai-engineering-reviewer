import re


def analyze_c_metrics(code: str, is_cpp: bool = False) -> dict:
    lines = code.splitlines()
    total = len(lines)
    blank = sum(1 for line in lines if not line.strip())
    # C/C++ single-line comment '//'
    comment = sum(1 for line in lines if line.strip().startswith("//") or line.strip().startswith("*"))
    code_lines = total - blank - comment

    # Very rough function detector: `return_type name(...)` on a single line followed by `{`
    function_pattern = r"\b\w[\w\s\*]*\s+(\w+)\s*\([^\)]*\)\s*\{"
    function_count = len(re.findall(function_pattern, code))

    # C++ class detection
    class_count = 0
    if is_cpp:
        class_count = len(re.findall(r"\bclass\s+\w+", code))
        class_count += len(re.findall(r"\bstruct\s+\w+", code))

    comment_ratio = round((comment / total) * 100, 1) if total else 0.0

    return {
        "total_lines": total,
        "code_lines": code_lines,
        "comment_lines": comment,
        "blank_lines": blank,
        "function_count": function_count,
        "class_count": class_count,
        "comment_ratio_pct": comment_ratio,
    }


def analyze_c_complexity(code: str) -> dict:
    decision_pattern = r"\b(if|for|while|case|switch|&&|\|\|)\b"
    total_decisions = len(re.findall(decision_pattern, code))

    est_cyclomatic = 1 + total_decisions

    depth = 0
    cognitive = 0
    for line in code.splitlines():
        stripped = line.strip()
        opens = stripped.count("{")
        closes = stripped.count("}")

        for _ in re.findall(decision_pattern, stripped):
            cognitive += 1 + depth

        depth += opens - closes
        depth = max(0, depth)

    if est_cyclomatic <= 5 and cognitive <= 8:
        verdict = "simple"
    elif est_cyclomatic <= 15 and cognitive <= 20:
        verdict = "moderate"
    else:
        verdict = "complex"

    return {
        "cyclomatic": {"per_function": [], "max": est_cyclomatic},
        "cognitive": {"per_function": [], "max": cognitive},
        "verdict": verdict,
        "findings": [],
        "note": "C/C++ complexity is estimated at file level (regex-based).",
    }


def check_c_cpp_security(code: str) -> list:
    findings = []
    patterns = [
        {
            "pattern": r"\bgets\s*\(",
            "title": "Use of gets()",
            "severity": "critical",
            "reason": "gets() reads unlimited input into a buffer with no bounds check.",
            "impact": "Classic buffer overflow. Never safe.",
            "recommendation": "Use fgets() with a size limit instead.",
        },
        {
            "pattern": r"\bstrcpy\s*\(",
            "title": "Use of strcpy()",
            "severity": "high",
            "reason": "strcpy() performs no bounds checking on the destination buffer.",
            "impact": "Can cause buffer overflows if source is longer than destination.",
            "recommendation": "Use strncpy() or strlcpy() with an explicit size limit.",
        },
        {
            "pattern": r"\bstrcat\s*\(",
            "title": "Use of strcat()",
            "severity": "high",
            "reason": "strcat() performs no bounds checking on the destination.",
            "impact": "Can cause buffer overflows.",
            "recommendation": "Use strncat() or strlcat() with an explicit size limit.",
        },
        {
            "pattern": r"\bsprintf\s*\(",
            "title": "Use of sprintf()",
            "severity": "high",
            "reason": "sprintf() writes to a buffer with no size limit.",
            "impact": "Can cause buffer overflows if formatted output exceeds buffer size.",
            "recommendation": "Use snprintf() with an explicit size limit.",
        },
        {
            "pattern": r"\bsystem\s*\(",
            "title": "Use of system()",
            "severity": "high",
            "reason": "system() invokes a shell to run the command.",
            "impact": "Enables command injection if the argument comes from untrusted input.",
            "recommendation": "Use exec-family functions with argument arrays and no shell.",
        },
        {
            "pattern": r"\bscanf\s*\(\s*\"[^\"]*%s",
            "title": "scanf() with unbounded %s",
            "severity": "high",
            "reason": "scanf(\"%s\", ...) has no length limit on the input.",
            "impact": "Buffer overflow.",
            "recommendation": "Specify a maximum field width: scanf(\"%99s\", buf).",
        },
    ]

    lines = code.splitlines()
    for entry in patterns:
        for i, line in enumerate(lines, start=1):
            if re.search(entry["pattern"], line):
                findings.append({
                    "title": entry["title"],
                    "category": "Security",
                    "severity": entry["severity"],
                    "location": {"line": i},
                    "reason": entry["reason"],
                    "impact": entry["impact"],
                    "recommendation": entry["recommendation"],
                })
    return findings


def analyze_c_maintainability(code: str) -> dict:
    findings = []
    lines = code.splitlines()

    LONG_LINE = 120
    for i, line in enumerate(lines, start=1):
        if len(line) > LONG_LINE:
            findings.append({
                "title": "Line exceeds recommended length",
                "category": "Maintainability",
                "severity": "low",
                "location": {"line": i},
                "reason": f"Line {i} is {len(line)} characters long (limit {LONG_LINE}).",
                "impact": "Long lines are harder to read and review.",
                "recommendation": f"Wrap the line to stay under {LONG_LINE} characters.",
            })
        s = line.strip()
        if "TODO" in s or "FIXME" in s:
            findings.append({
                "title": "Unresolved TODO/FIXME",
                "category": "Maintainability",
                "severity": "low",
                "location": {"line": i},
                "reason": f"Line {i} contains a TODO or FIXME marker.",
                "impact": "Unresolved markers indicate incomplete work.",
                "recommendation": "Track the item and remove the marker once addressed.",
            })

    return {
        "docstring_coverage_pct": None,
        "findings": findings,
        "note": "C/C++ maintainability uses regex heuristics (docstring coverage not applicable).",
    }