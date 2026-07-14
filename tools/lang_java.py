import re


def analyze_java_metrics(code: str) -> dict:
    lines = code.splitlines()
    total = len(lines)
    blank = sum(1 for line in lines if not line.strip())
    # Java has // and /* */ comments; treat // as a comment line
    comment = sum(1 for line in lines if line.strip().startswith("//") or line.strip().startswith("*"))
    code_lines = total - blank - comment

    # Very rough: count `class X` and method signatures.
    class_count = len(re.findall(r"\bclass\s+\w+", code))
    method_count = len(re.findall(
        r"\b(public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\([^\)]*\)\s*(throws\s+[\w,\s]+)?\s*\{",
        code,
    ))

    comment_ratio = round((comment / total) * 100, 1) if total else 0.0

    return {
        "total_lines": total,
        "code_lines": code_lines,
        "comment_lines": comment,
        "blank_lines": blank,
        "function_count": method_count,
        "class_count": class_count,
        "comment_ratio_pct": comment_ratio,
    }


def analyze_java_complexity(code: str) -> dict:
    """
    Regex-based estimate — counts decision keywords across the file.
    Not per-function like the Python AST version. Honest limitation.
    """
    decision_pattern = r"\b(if|for|while|case|catch|&&|\|\|)\b"
    total_decisions = len(re.findall(decision_pattern, code))

    # Cyclomatic-ish: 1 + number of decisions in the whole file
    est_cyclomatic = 1 + total_decisions

    # Cognitive-ish: penalize nested blocks by depth
    depth = 0
    max_depth = 0
    cognitive = 0
    for line in code.splitlines():
        stripped = line.strip()
        opens = stripped.count("{")
        closes = stripped.count("}")

        # Score decision keywords weighted by depth
        for _ in re.findall(decision_pattern, stripped):
            cognitive += 1 + depth

        depth += opens - closes
        depth = max(0, depth)
        max_depth = max(max_depth, depth)

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
        "note": "Java complexity is estimated at file level (regex-based).",
    }


def check_java_security(code: str) -> list:
    findings = []
    patterns = [
        {
            "pattern": r"Runtime\.getRuntime\(\)\.exec\(",
            "title": "Use of Runtime.exec()",
            "severity": "high",
            "reason": "Runtime.exec() spawns a process from a command string.",
            "impact": "If the command string comes from untrusted input, this allows command injection.",
            "recommendation": "Use ProcessBuilder with an argument list and validate all input.",
        },
        {
            "pattern": r"\.executeQuery\s*\(\s*\"[^\"]*\"\s*\+",
            "title": "SQL query built with string concatenation",
            "severity": "critical",
            "reason": "SQL queries built by concatenating strings are vulnerable to SQL injection.",
            "impact": "Attackers can inject SQL and read or modify the database.",
            "recommendation": "Use PreparedStatement with parameter binding instead of concatenation.",
        },
        {
            "pattern": r"MessageDigest\.getInstance\(\s*\"MD5\"\s*\)",
            "title": "Use of MD5 hashing",
            "severity": "medium",
            "reason": "MD5 is cryptographically broken and unsuitable for security.",
            "impact": "Using MD5 for password hashing or integrity is insecure.",
            "recommendation": "Use SHA-256 or better, and for passwords use bcrypt/scrypt/Argon2.",
        },
        {
            "pattern": r"new\s+Random\s*\(\s*\)",
            "title": "Use of java.util.Random",
            "severity": "low",
            "reason": "java.util.Random is not cryptographically secure.",
            "impact": "Predictable random values in a security context can be exploited.",
            "recommendation": "Use java.security.SecureRandom for security-sensitive randomness.",
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


def analyze_java_maintainability(code: str) -> dict:
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

    # Java docstring proxy: count javadoc /** comments vs method signatures
    method_count = len(re.findall(
        r"\b(public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\([^\)]*\)\s*(throws\s+[\w,\s]+)?\s*\{",
        code,
    ))
    javadoc_count = len(re.findall(r"/\*\*", code))
    if method_count > 0:
        coverage = round(min(100, (javadoc_count / method_count) * 100), 1)
    else:
        coverage = None

    return {
        "docstring_coverage_pct": coverage,
        "findings": findings,
        "note": "Java maintainability uses regex heuristics (not full AST).",
    }
