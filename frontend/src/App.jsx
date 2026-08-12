import { useState, useEffect } from "react";

import Header from "./components/Header";
import DashboardStats from "./components/DashboardStats";
import MonacoEditor from "./components/MonacoEditor";
import A2UIRenderer from "./components/A2UIRenderer";
import HistoryChart from "./components/HistoryChart";
import ExportButtons from "./components/ExportButtons";

import {
  runReview,
  generateRefactor,
  getHistory,
} from "./api/reviewApi";

import "./index.css";

function App() {
  const [code, setCode] = useState(`def hello():
    print("Hello World")
`);

  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  const [loading, setLoading] = useState(false);

  const [refactoredCode, setRefactoredCode] =
    useState("");

  const [refactorLoading, setRefactorLoading] =
    useState(false);
  const [verifiedRefactor, setVerifiedRefactor] =
  useState(null);


  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await getHistory();
        setHistory(data);
      } catch (err) {
        console.error(err);
      }
    }

    loadHistory();
  }, []);

  async function handleReview() {
    try {
      setLoading(true);
      const data = await runReview(code);

setResult(data);

const updatedHistory =
  await getHistory();
  console.log(updatedHistory.length);

setHistory(updatedHistory);

      
    } catch (err) {
  console.error("FULL ERROR:", err);

  alert(
    JSON.stringify(
      err?.response?.data ||
      err?.message ||
      err,
      null,
      2
    )
  );
} finally {
      setLoading(false);
    }
  }

  async function handleRefactor() {
  try {
    setRefactorLoading(true);

    const data =
      await generateRefactor(
        code
      );

    console.log(data);

    setVerifiedRefactor(data);

    setRefactoredCode(
      data.refactored_code || ""
    );

  } catch (err) {
    console.error(err);

    alert(
      "Failed to generate refactor"
    );
  } finally {
    setRefactorLoading(false);
  }
}

  return (
    <div className="app">
      <Header />

      <DashboardStats
  reviews={history.length}
  bestScore={
    history.length
      ? Math.max(
          ...history.map(
            (item) => item.score
          )
        )
      : 0
  }
/>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "2fr 1fr",
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
          <h2>
            Project Insights
          </h2>

          <p
            style={{
              color: "#9ca3af",
              marginBottom: "20px",
            }}
          >
            MCP-Powered Engineering
            Intelligence
          </p>

          <div
            style={{
              display: "flex",
              flexDirection:
                "column",
              gap: "12px",
            }}
          >
            <div>
              ✅ Multi-Language
              Analysis
            </div>

            <div>
              ✅ Security Review
            </div>

            <div>
              ✅ Complexity Detection
            </div>

            <div>
              ✅ AI Reasoning Engine
            </div>

            <div>
              ✅ Company Rule
              Validation
            </div>

            <div>
              ✅ Engineering Score
            </div>
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
              : "linear-gradient(135deg,#2563eb,#1d4ed8)",
            color: "white",
            border: "none",
            padding:
              "14px 32px",
            borderRadius:
              "12px",
            fontSize: "16px",
            fontWeight: "700",
            cursor: loading
              ? "not-allowed"
              : "pointer",
            boxShadow:
              "0 8px 20px rgba(37,99,235,.3)",
          }}
        >
          {loading
            ? "🔄 Running Review..."
            : "🚀 Run Engineering Review"}
        </button>

        <button
          onClick={handleRefactor}
          disabled={
            refactorLoading
          }
          style={{
            background:
              "linear-gradient(135deg,#16a34a,#15803d)",
            color: "white",
            border: "none",
            padding:
              "14px 32px",
            borderRadius:
              "12px",
            fontSize: "16px",
            fontWeight: "700",
            cursor: "pointer",
            boxShadow:
              "0 8px 20px rgba(22,163,74,.3)",
          }}
        >
          {refactorLoading
            ? "🔄 Refactoring..."
            : "✨ Generate Refactor"}
        </button>
      </div>

      {loading && (
        <div className="loading-banner">
          🔄 Running AI
          Engineering Review...
        </div>
      )}

      {refactorLoading && (
        <div className="loading-banner">
          ✨ Generating
          Refactored Code...
        </div>
      )}

      {result?.components && (
        <A2UIRenderer
          components={
            result.components
          }
        />
      )}
      {verifiedRefactor && (
  <div className="card">
    <h2>
      ✅ Verified Refactor
    </h2>

    <p>
      Original Score:
      {" "}
      <strong>
        {verifiedRefactor.original_score}
      </strong>
    </p>

    <p>
      Refactored Score:
      {" "}
      <strong>
        {verifiedRefactor.refactored_score}
      </strong>
    </p>

    <p>
      Improvement:
      {" "}
      <strong>
        {verifiedRefactor.score_delta}
      </strong>
    </p>
  </div>
)}
      {refactoredCode && (
        <div className="card">
          <h2>
            ✨ Refactored Code
          </h2>

          <pre
            style={{
              whiteSpace:
                "pre-wrap",
              overflowX: "auto",
              background:
                "#111827",
              padding: "16px",
              borderRadius:
                "12px",
              color:
                "#e5e7eb",
              border:
                "1px solid #374151",
            }}
          >
            {refactoredCode}
          </pre>
        </div>
      )}

      <HistoryChart
        history={history}
      />

      <ExportButtons />
    </div>
  );
}

export default App;