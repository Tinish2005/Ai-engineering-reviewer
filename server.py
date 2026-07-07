import json
from mcp.server.fastmcp import FastMCP

from tools import (
    analyze_metrics,
    analyze_complexity,
    check_security,
    analyze_maintainability,
    check_company_rules as _check_company_rules,
)
from core import run_review
from ai_layer import generate_review_reasoning, generate_fixed_code

mcp = FastMCP("AI Engineering Reviewer")


@mcp.tool()
def get_metrics(code: str) -> dict:
    """Compute size and structure metrics for the given code."""
    return analyze_metrics(code)


@mcp.tool()
def get_complexity(code: str) -> dict:
    """Compute cyclomatic and cognitive complexity per function."""
    return analyze_complexity(code)


@mcp.tool()
def get_security(code: str) -> list:
    """Detect risky security patterns."""
    return check_security(code)


@mcp.tool()
def get_maintainability(code: str) -> dict:
    """Analyze maintainability issues."""
    return analyze_maintainability(code)


@mcp.tool()
def check_company_rules(code: str) -> dict:
    """Check code against company rules from rules.yaml."""
    review_data = {
        "metrics": analyze_metrics(code),
        "complexity": analyze_complexity(code),
        "security": check_security(code),
        "maintainability": analyze_maintainability(code),
    }
    return _check_company_rules(code, review_data)


@mcp.tool()
def get_ai_reasoning(review_data: str) -> dict:
    """Use Gemini to reason over deterministic findings."""
    try:
        data = json.loads(review_data)
    except Exception:
        return {"summary": "Invalid JSON.", "priority_issues": [], "suggestions": []}
    return generate_review_reasoning(data)


@mcp.tool()
def full_review(code: str) -> dict:
    """Run the full engineering review pipeline."""
    return run_review(code)


@mcp.tool()
def generate_refactored_code(code: str) -> str:
    """Return a refactored version of the code."""
    review_data = {
        "metrics": analyze_metrics(code),
        "complexity": analyze_complexity(code),
        "security": check_security(code),
        "maintainability": analyze_maintainability(code),
    }
    return generate_fixed_code(code, review_data)


if __name__ == "__main__":
    mcp.run()
