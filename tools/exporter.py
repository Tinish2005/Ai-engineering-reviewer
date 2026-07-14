import json
from pathlib import Path

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)


def export_json(review):
    path = EXPORT_DIR / "latest_review.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(review, f, indent=2)

    return str(path)


def export_markdown(review):
    path = EXPORT_DIR / "latest_review.md"

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Engineering Review\n\n")

        for component in review.get("components", []):

            title = component.get(
                "title",
                component.get("type", "Unknown")
            )

            f.write(f"## {title}\n\n")
            f.write(
                "```json\n"
                + json.dumps(component, indent=2)
                + "\n```\n\n"
            )

    return str(path)