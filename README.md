# AI Engineering Review Platform

A real MCP-driven AI Engineering Review Platform that turns raw code into a structured engineering review using deterministic engineering tools, Gemini AI reasoning, and A2UI-structured JSON.

Two independent interfaces share the same MCP backbone:

- ✅ **Flask + A2UI product UI** — for real users
- ✅ **Claude Desktop MCP client** — for AI-driven usage

Both interfaces call the same shared engineering brain (`core.py`), so no logic is duplicated.

---

## 🏗 Architecture