function AISummary({
  title,
  summary,
  priority_issues = [],
  suggestions = [],
}) {
  return (
    <div className="card">
      <h2>{title}</h2>

      {/* Summary */}
      <div className="summary-section">
        <h3>📋 Summary</h3>

        <div className="finding-card">
          <p>{summary}</p>
        </div>
      </div>

      {/* Priority Issues */}
      <div className="summary-section">
        <h3>⚠ Priority Issues</h3>

        {priority_issues.length === 0 ? (
          <div className="success-box">
            ✅ No Critical Issues Found
          </div>
        ) : (
          priority_issues.map((issue, index) => (
            <div
              key={index}
              className="finding-card"
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: "12px",
                }}
              >
                <h3>{issue.title}</h3>

                <span
                  style={{
                    background:
                      issue.severity === "critical"
                        ? "#991b1b"
                        : issue.severity === "high"
                        ? "#dc2626"
                        : issue.severity === "medium"
                        ? "#ca8a04"
                        : "#2563eb",
                    color: "white",
                    padding: "4px 10px",
                    borderRadius: "999px",
                    fontWeight: "bold",
                    fontSize: "12px",
                  }}
                >
                  {issue.severity?.toUpperCase()}
                </span>
              </div>

              <p>
                <strong>Reason:</strong>{" "}
                {issue.reason ||
                  "No detailed reason was provided by the AI engine."}
              </p>

              <p>
                <strong>Impact:</strong>{" "}
                {issue.impact ||
                  "See recommendation section for additional guidance."}
              </p>
            </div>
          ))
        )}
      </div>

      {/* Suggestions */}
      <div className="summary-section">
        <h3>💡 Recommendations</h3>

        {suggestions.length === 0 ? (
          <div className="success-box">
            No Recommendations Available
          </div>
        ) : (
          suggestions.map((suggestion, index) => (
            <div
              key={index}
              className="finding-card"
            >
              {typeof suggestion === "string" ? (
                <p>{suggestion}</p>
              ) : (
                <>
                  <h3>
                    {suggestion.area ||
                      "Recommendation"}
                  </h3>

                  <p>
                    {suggestion.recommendation ||
                      suggestion.text ||
                      "No recommendation text provided."}
                  </p>

                  {suggestion.related_issue && (
                    <p
                      style={{
                        color: "#9ca3af",
                        marginTop: "10px",
                      }}
                    >
                      <strong>
                        Related Issue:
                      </strong>{" "}
                      {suggestion.related_issue}
                    </p>
                  )}
                </>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default AISummary;