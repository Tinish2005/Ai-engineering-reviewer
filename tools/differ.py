import difflib


def compute_diff(original: str, refactored: str) -> dict:
    """
    Compute a side-by-side diff between original and refactored code.

    Returns a dict with:
      - "lines": a list of aligned line pairs (each pair may have None on one side)
      - "stats": counts of added/removed/unchanged lines
    """
    original_lines = original.splitlines()
    refactored_lines = refactored.splitlines()

    matcher = difflib.SequenceMatcher(a=original_lines, b=refactored_lines, autojunk=False)

    lines = []
    added = 0
    removed = 0
    unchanged = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                lines.append({
                    "left_num": i1 + k + 1,
                    "left_text": original_lines[i1 + k],
                    "right_num": j1 + k + 1,
                    "right_text": refactored_lines[j1 + k],
                    "kind": "unchanged",
                })
                unchanged += 1

        elif tag == "delete":
            for k in range(i2 - i1):
                lines.append({
                    "left_num": i1 + k + 1,
                    "left_text": original_lines[i1 + k],
                    "right_num": None,
                    "right_text": "",
                    "kind": "removed",
                })
                removed += 1

        elif tag == "insert":
            for k in range(j2 - j1):
                lines.append({
                    "left_num": None,
                    "left_text": "",
                    "right_num": j1 + k + 1,
                    "right_text": refactored_lines[j1 + k],
                    "kind": "added",
                })
                added += 1

        elif tag == "replace":
            # Pair replacements line-by-line; if lengths differ, pad with blanks.
            left_count = i2 - i1
            right_count = j2 - j1
            max_count = max(left_count, right_count)
            for k in range(max_count):
                left_num = (i1 + k + 1) if k < left_count else None
                left_text = original_lines[i1 + k] if k < left_count else ""
                right_num = (j1 + k + 1) if k < right_count else None
                right_text = refactored_lines[j1 + k] if k < right_count else ""

                if left_num is not None and right_num is not None:
                    lines.append({
                        "left_num": left_num,
                        "left_text": left_text,
                        "right_num": right_num,
                        "right_text": right_text,
                        "kind": "changed",
                    })
                    added += 1
                    removed += 1
                elif left_num is not None:
                    lines.append({
                        "left_num": left_num,
                        "left_text": left_text,
                        "right_num": None,
                        "right_text": "",
                        "kind": "removed",
                    })
                    removed += 1
                else:
                    lines.append({
                        "left_num": None,
                        "left_text": "",
                        "right_num": right_num,
                        "right_text": right_text,
                        "kind": "added",
                    })
                    added += 1

    return {
        "lines": lines,
        "stats": {
            "added": added,
            "removed": removed,
            "unchanged": unchanged,
            "total_original": len(original_lines),
            "total_refactored": len(refactored_lines),
        },
    }