def detect_smells(code: str) -> list:
    smells = []
    lines = code.splitlines()

    for i, line in enumerate(lines, start=1):
        if len(line) > 120:
            smells.append({"line": i, "issue": "Line too long"})
        if "TODO" in line or "FIXME" in line:
            smells.append({"line": i, "issue": "Unresolved TODO/FIXME"})
        if line.strip().startswith("def ") and "(" in line and len(line.split(",")) > 6:
            smells.append({"line": i, "issue": "Too many function parameters"})

    return smells