import mcp_client

mcp_client.start()
try:
    result = mcp_client.call_tool(
        "full_review",
        {"code": 'def add(a, b):\n    eval("1+1")\n    return a + b\n'},
    )
    print("type:", result.get("type"))
    print("components:", len(result.get("components", [])))
finally:
    mcp_client.stop()
