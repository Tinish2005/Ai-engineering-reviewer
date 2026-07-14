import { useState } from "react";

import Header from "./components/Header";
import DashboardStats from "./components/DashboardStats";
import MonacoEditor from "./components/MonacoEditor";
import A2UIRenderer from "./components/A2UIRenderer";

import { runReview } from "./api/reviewApi";

import "./index.css";

function App() {
  const [code, setCode] = useState(`def hello():
    print("Hello World")
`);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleReview() {
    try {
      setLoading(true);

      const data = await runReview(code);

      console.log(data);

      setResult(data);
    } catch (err) {
      console.error(err);

      alert("Failed to connect to Flask backend");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <Header />

      <DashboardStats />

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: "24px",
          marginBottom: "24px",
          alignItems: "start",
        }}
      >
        <div>
          <MonacoEditor
            value={code}
            onChange={setCode}
          />
        </div>

        <div className="card">
          <h2>Project Insights</h2>

          <p
            style={{
              color: "#9ca3af",
              marginBottom: "20px",
            }}
          >
            MCP-Powered Engineering Intelligence
          </p>

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "12px",
            }}
          >
            <div>✅ Multi-Language Analysis</div>
            <div>✅ Security Review</div>
            <div>✅ Complexity Detection</div>
            <div>✅ AI Reasoning Engine</div>
            <div>✅ Company Rule Validation</div>
            <div>✅ Engineering Score</div>
          </div>
        </div>
      </div>

      <div
        style={{
          display: "flex",
          gap: "16px",
          marginBottom: "20px",
          flexWrap: "wrap",
        }}
      >
        <button
          onClick={handleReview}
          disabled={loading}
          style={{
            background: loading
              ? "#6b7280"
              : "#2563eb",
            color: "white",
            border: "none",
            padding: "14px 28px",
            borderRadius: "12px",
            fontSize: "16px",
            fontWeight: "600",
            cursor: loading
              ? "not-allowed"
              : "pointer",
          }}
        >
          {loading
            ? "🔄 Running Review..."
            : "🚀 Run Engineering Review"}
        </button>

        <button
          disabled
          style={{
            background: "#16a34a",
            color: "white",
            border: "none",
            padding: "14px 28px",
            borderRadius: "12px",
            fontSize: "16px",
            fontWeight: "600",
            opacity: 0.6,
            cursor: "not-allowed",
          }}
        >
          🚧 Generate Refactor (Coming Soon)
        </button>
      </div>

      {loading && (
        <div className="loading-banner">
          🔄 Running AI Engineering Review...
        </div>
      )}

      {result?.components && (
        <A2UIRenderer
          components={result.components}
        />
      )}
    </div>
  );
}

export default App;