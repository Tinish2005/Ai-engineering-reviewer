from core import run_review

code = 'def add(a, b):\n    eval("1+1")\n    return a + b\n'
result = run_review(code)
print("type:", result["type"])
print("components:", len(result["components"]))
for c in result["components"]:
    print("  -", c["type"], "::", c.get("title"))