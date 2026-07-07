import sys
print("STEP 1: app.py starting", flush=True)
sys.stdout.flush()

try:
    import atexit
    print("STEP 2: atexit imported", flush=True)

    from flask import Flask, request, jsonify, render_template
    print("STEP 3: flask imported", flush=True)

    import mcp_client
    print("STEP 4: mcp_client imported", flush=True)

    app = Flask(__name__)
    print("STEP 5: Flask app created", flush=True)

    print("STEP 6: calling mcp_client.start() ...", flush=True)
    mcp_client.start()
    print("STEP 7: mcp_client started successfully", flush=True)

    atexit.register(mcp_client.stop)
    print("STEP 8: atexit registered", flush=True)


    @app.route("/")
    def home():
        return render_template("index.html")


    @app.route("/review", methods=["POST"])
    def review():
        data = request.get_json(force=True) or {}
        code = data.get("code", "")
        if not code.strip():
            return jsonify({"type": "error", "message": "Empty code submitted."}), 400
        try:
            result = mcp_client.call_tool("full_review", {"code": code})
        except Exception as e:
            return jsonify({"type": "error", "message": f"MCP call failed: {e}"}), 500
        if result is None:
            return jsonify({"type": "error", "message": "Empty response from MCP tool."}), 500
        return jsonify(result)


    @app.route("/refactor", methods=["POST"])
    def refactor_code():
        data = request.get_json(force=True) or {}
        code = data.get("code", "")
        if not code.strip():
            return jsonify({"type": "error", "message": "Empty code submitted."}), 400
        try:
            refactored = mcp_client.call_tool("generate_refactored_code", {"code": code})
        except Exception as e:
            return jsonify({"type": "error", "message": f"MCP call failed: {e}"}), 500
        return jsonify({
            "type": "code_card",
            "title": "Refactored Code",
            "code": refactored if isinstance(refactored, str) else str(refactored),
        })


    if __name__ == "__main__":
        print("STEP 9: about to start Flask server", flush=True)
        app.run(debug=True, use_reloader=False)

except Exception as e:
    print(f"CRASH: {type(e).__name__}: {e}", flush=True)
    import traceback
    traceback.print_exc()