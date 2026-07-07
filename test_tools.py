from tools import analyze_metrics, analyze_complexity, check_security, analyze_maintainability

code = '''
def add(a, b):
    eval("1+1")
    return a + b

def calculate(a, b, c, d, e, f, g):
    if a > b:
        if b > c:
            if c > d:
                if d > e:
                    return f * g
    return -1

def execute_command(cmd):
    import os
    os.system(cmd)

def load_data(filename):
    import pickle
    with open(filename, "rb") as f:
        return pickle.load(f)

# TODO: implement caching
'''

print("=== METRICS ===")
print(analyze_metrics(code))
print()

print("=== COMPLEXITY ===")
c = analyze_complexity(code)
print("verdict:", c["verdict"], "| max cyc:", c["cyclomatic"]["max"], "| max cog:", c["cognitive"]["max"])
print("findings:", len(c["findings"]))
for f in c["findings"]:
    print("  -", f["severity"], "|", f["title"], "| line", f["location"]["line"])
print()

print("=== SECURITY ===")
sec = check_security(code)
print("findings:", len(sec))
for f in sec:
    print("  -", f["severity"], "|", f["title"], "| line", f["location"]["line"])
print()

print("=== MAINTAINABILITY ===")
m = analyze_maintainability(code)
print("docstring coverage:", m["docstring_coverage_pct"], "%")
print("findings:", len(m["findings"]))
for f in m["findings"]:
    print("  -", f["severity"], "|", f["title"])