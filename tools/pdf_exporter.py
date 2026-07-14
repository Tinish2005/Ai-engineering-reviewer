from pathlib import Path
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)


def export_pdf(review):

    path = EXPORT_DIR / "latest_review.pdf"

    doc = SimpleDocTemplate(
        str(path)
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Engineering Review Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    for component in review.get(
        "components",
        []
    ):

        title = component.get(
            "title",
            component.get(
                "type",
                "Unknown"
            )
        )

        content.append(
            Paragraph(
                title,
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                str(component),
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 6)
        )

    doc.build(content)

    return str(path)