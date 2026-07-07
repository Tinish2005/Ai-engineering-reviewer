def analyze_metrics(code: str) -> dict:
    lines = code.splitlines()
    total = len(lines)
    blank = sum(1 for line in lines if not line.strip())
    comment = sum(1 for line in lines if line.strip().startswith("#"))
    code_lines = total - blank - comment

    function_count = 0
    class_count = 0
    for line in lines:
        s = line.strip()
        if s.startswith("def ") or s.startswith("async def "):
            function_count += 1
        elif s.startswith("class "):
            class_count += 1

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