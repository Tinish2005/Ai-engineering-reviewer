import sys
from flask_cors import CORS

print("STEP 1: app.py starting", flush=True)

try:
    import atexit

    print("STEP 2: atexit imported", flush=True)

    from flask import (
        Flask,
        request,
        jsonify,
        render_template,
    )

    print("STEP 3: flask imported", flush=True)

    import mcp_client

    print("STEP 4: mcp_client imported", flush=True)

    from tools.history import (
        initialize_database,
        get_recent_reviews,
        get_review,
    )

    print("STEP 5: history imported", flush=True)

    from tools.exporter import (
        export_json,
        export_markdown,
    )

    print("STEP 6: exporter imported", flush=True)

    from tools.pdf_exporter import (
        export_pdf,
    )

    print("STEP 7: pdf exporter imported", flush=True)

    app = Flask(__name__)
    CORS(app)

    print("STEP 8: Flask app created", flush=True)

    initialize_database()

    print("STEP 9: database initialized", flush=True)

    print("STEP 10: starting MCP client...", flush=True)

    mcp_client.start()

    print("STEP 11: MCP client started", flush=True)

    atexit.register(mcp_client.stop)

    print("STEP 12: atexit registered", flush=True)

    # =================================================
    # HOME
    # =================================================

    @app.route("/")
    def home():
        return render_template("index.html")

    # =================================================
    # REVIEW
    # =================================================

    @app.route("/review", methods=["POST"])
    def review():

        data = request.get_json(force=True) or {}

        code = data.get("code", "")

        if not code.strip():
            return jsonify(
                {
                    "type": "error",
                    "message": "Empty code submitted.",
                }
            ), 400

        try:

            result = mcp_client.call_tool(
                "full_review",
                {
                    "code": code,
                },
            )

        except Exception as e:

            return jsonify(
                {
                    "type": "error",
                    "message": f"MCP call failed: {e}",
                }
            ), 500

        if result is None:

            return jsonify(
                {
                    "type": "error",
                    "message": "Empty response from MCP.",
                }
            ), 500

        return jsonify(result)

    # =================================================
    # REFACTOR
    # =================================================

    @app.route("/refactor", methods=["POST"])
    def refactor_code():

        data = request.get_json(force=True) or {}

        code = data.get("code", "")

        if not code.strip():
            return jsonify(
                {
                    "type": "error",
                    "message": "Empty code submitted.",
                }
            ), 400

        try:

            refactored = mcp_client.call_tool(
                "generate_refactored_code",
                {
                    "code": code,
                },
            )

        except Exception as e:

            return jsonify(
                {
                    "type": "error",
                    "message": f"MCP call failed: {e}",
                }
            ), 500

        return jsonify(
            {
                "type": "code_card",
                "title": "Refactored Code",
                "code": refactored,
            }
        )

    # =================================================
    # HISTORY
    # =================================================

    @app.route("/history")
    def history():
        return jsonify(
            get_recent_reviews()
        )

    # =================================================
    # EXPORT JSON
    # =================================================

    @app.route("/export/json/<int:review_id>")
    def export_review_json(review_id):

        review = get_review(review_id)

        if not review:
            return jsonify(
                {
                    "error": "Review not found",
                }
            ), 404

        path = export_json(
            review["result"]
        )

        return jsonify(
            {
                "file": path,
            }
        )

    # =================================================
    # EXPORT MARKDOWN
    # =================================================

    @app.route("/export/markdown/<int:review_id>")
    def export_review_markdown(review_id):

        review = get_review(review_id)

        if not review:
            return jsonify(
                {
                    "error": "Review not found",
                }
            ), 404

        path = export_markdown(
            review["result"]
        )

        return jsonify(
            {
                "file": path,
            }
        )

    # =================================================
    # EXPORT PDF
    # =================================================

    @app.route("/export/pdf/<int:review_id>")
    def export_review_pdf(review_id):

        review = get_review(review_id)

        if not review:
            return jsonify(
                {
                    "error": "Review not found",
                }
            ), 404

        path = export_pdf(
            review["result"]
        )

        return jsonify(
            {
                "file": path,
            }
        )

    # =================================================
    # START APP
    # =================================================

    if __name__ == "__main__":

        print(
            "STEP 13: about to start Flask server",
            flush=True,
        )

        app.run(
            debug=True,
            use_reloader=False,
        )

except Exception as e:

    print(
        f"CRASH: {type(e).__name__}: {e}",
        flush=True,
    )

    import traceback

    traceback.print_exc()

 