import re


def detect_language(code: str) -> str:
    """
    Detect the language of the given code by looking for language-specific patterns.
    Returns one of: "python", "java", "c", "cpp", or "unknown".

    Uses a scoring system so that a single ambiguous line doesn't misclassify.
    """
    if not code.strip():
        return "unknown"

    scores = {"python": 0, "java": 0, "c": 0, "cpp": 0}

    # Python-specific signals
    if re.search(r"^\s*def\s+\w+\s*\(", code, re.MULTILINE):
        scores["python"] += 3
    if re.search(r"^\s*from\s+\w+\s+import\s+", code, re.MULTILINE):
        scores["python"] += 3
    if re.search(r"^\s*import\s+\w+(\s*,\s*\w+)*\s*$", code, re.MULTILINE):
        scores["python"] += 2
    if re.search(r"^\s*class\s+\w+\s*(\([^)]*\))?\s*:", code, re.MULTILINE):
        scores["python"] += 3
    if re.search(r"#.*$", code, re.MULTILINE):
        scores["python"] += 1
    if re.search(r"\bprint\s*\(", code):
        scores["python"] += 1
    if re.search(r":\s*$", code, re.MULTILINE):
        # Python uses ':' at end of block-opening lines
        scores["python"] += 2

    # Java-specific signals
    if re.search(r"^\s*public\s+class\s+\w+", code, re.MULTILINE):
        scores["java"] += 5
    if re.search(r"^\s*package\s+[\w.]+\s*;", code, re.MULTILINE):
        scores["java"] += 4
    if re.search(r"^\s*import\s+[\w.]+\s*;", code, re.MULTILINE):
        scores["java"] += 3
    if re.search(r"public\s+static\s+void\s+main\s*\(\s*String", code):
        scores["java"] += 5
    if re.search(r"\bSystem\.out\.print", code):
        scores["java"] += 3
    if re.search(r"@\w+", code) and "class" in code:
        scores["java"] += 1

    # C++-specific signals (checked before C so C++ wins the tiebreak)
    if re.search(r"#include\s*<iostream>", code):
        scores["cpp"] += 5
    if re.search(r"#include\s*<vector>|#include\s*<string>|#include\s*<map>", code):
        scores["cpp"] += 3
    if re.search(r"\bstd::\w+", code):
        scores["cpp"] += 4
    if re.search(r"\busing\s+namespace\s+std\s*;", code):
        scores["cpp"] += 4
    if re.search(r"\bcout\s*<<", code) or re.search(r"\bcin\s*>>", code):
        scores["cpp"] += 4
    if re.search(r"^\s*class\s+\w+\s*(:\s*(public|private|protected))?", code, re.MULTILINE):
        scores["cpp"] += 2

    # C-specific signals
    if re.search(r"#include\s*<stdio\.h>", code):
        scores["c"] += 5
    if re.search(r"#include\s*<stdlib\.h>|#include\s*<string\.h>", code):
        scores["c"] += 3
    if re.search(r"\bprintf\s*\(", code):
        scores["c"] += 3
    if re.search(r"\bscanf\s*\(", code):
        scores["c"] += 3
    if re.search(r"\bint\s+main\s*\(", code):
        scores["c"] += 2  # also true in C++ but common in C
    if re.search(r"\bmalloc\s*\(|\bfree\s*\(", code):
        scores["c"] += 2
    if re.search(r"^\s*typedef\s+struct", code, re.MULTILINE):
        scores["c"] += 2

    # C and C++ share braces + semicolons — these help disambiguate from Python
    brace_lines = len(re.findall(r"[{}]", code))
    semi_lines = len(re.findall(r";\s*$", code, re.MULTILINE))
    if brace_lines > 3 and semi_lines > 3:
        scores["c"] += 1
        scores["cpp"] += 1

    # Pick the highest-scoring language, but require a minimum confidence
    best = max(scores, key=scores.get)
    if scores[best] < 3:
        return "unknown"
    return best


LANGUAGE_LABELS = {
    "python": "Python",
    "java": "Java",
    "c": "C",
    "cpp": "C++",
    "unknown": "Unknown",
}


def language_label(lang: str) -> str:
    return LANGUAGE_LABELS.get(lang, lang.title())