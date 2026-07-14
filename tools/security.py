from .language_detector import detect_language
from .lang_java import check_java_security
from .lang_c_cpp import check_c_cpp_security


_PATTERNS = [
    {
        "pattern": "eval(",
        "title": "Use of eval()",
        "severity": "critical",
        "reason": "eval() executes arbitrary strings as Python code.",
        "impact": "If any part of the input is user-controlled, this allows arbitrary code execution.",
        "recommendation": "Use ast.literal_eval() for parsing literals, or remove entirely.",
    },
    {
        "pattern": "exec(",
        "title": "Use of exec()",
        "severity": "critical",
        "reason": "exec() executes arbitrary Python code from a string.",
        "impact": "Allows arbitrary code execution if the input is not fully trusted.",
        "recommendation": "Redesign to avoid dynamic code execution. Use explicit dispatch tables instead.",
    },
    {
        "pattern": "pickle.load",
        "title": "Use of pickle.load",
        "severity": "critical",
        "reason": "pickle deserialization can invoke arbitrary constructors from the input stream.",
        "impact": "Loading pickled data from an untrusted source can result in remote code execution.",
        "recommendation": "Use json.load or another safe format for untrusted data.",
    },
    {
        "pattern": "os.system",
        "title": "Use of os.system()",
        "severity": "high",
        "reason": "os.system() runs commands through the shell without argument separation.",
        "impact": "Enables shell injection if any part of the command comes from untrusted input.",
        "recommendation": "Use subprocess.run(shlex.split(cmd), shell=False) and pass arguments as a list.",
    },
    {
        "pattern": "shell=True",
        "title": "subprocess called with shell=True",
        "severity": "high",
        "reason": "shell=True runs the command via a shell, which interprets metacharacters.",
        "impact": "Enables shell injection if any part of the command comes from untrusted input.",
        "recommendation": "Set shell=False (the default) and pass args as a list.",
    },
]


def check_security(code: str, language: str = None) -> list:
    """
    Detect risky security patterns.
    Dispatches to language-specific checker.
    """
    if language is None:
        language = detect_language(code)

    if language == "java":
        return check_java_security(code)
    if language in ("c", "cpp"):
        return check_c_cpp_security(code)

    # Python (and unknown, as fallback)
    findings = []
    lines = code.splitlines()
    for entry in _PATTERNS:
        pat = entry["pattern"]
        for line_num, line in enumerate(lines, start=1):
            if pat in line:
                findings.append({
                    "title": entry["title"],
                    "category": "Security",
                    "severity": entry["severity"],
                    "location": {"line": line_num},
                    "reason": entry["reason"],
                    "impact": entry["impact"],
                    "recommendation": entry["recommendation"],
                })
    return findings