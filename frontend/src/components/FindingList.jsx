function FindingList({
  title,
  findings = [],
}) {
  return (
    <div className="card">
      <h2>{title}</h2>

      {findings.length === 0 ? (
        <div className="success-box">
          ✅ No Findings Detected
        </div>
      ) : (
        findings.map((finding, index) => (
          <div
            key={index}
            className="finding-card"
          >
            <div
              style={{
                display: "flex",
                justifyContent:
                  "space-between",
                alignItems: "center",
              }}
            >
              <h3>{finding.title}</h3>

              <span
                style={{
                  background:
                    finding.severity === "high"
                      ? "#dc2626"
                      : finding.severity ===
                        "medium"
                      ? "#ca8a04"
                      : "#2563eb",
                  color: "white",
                  padding:
                    "4px 10px",
                  borderRadius:
                    "999px",
                }}
              >
                {finding.severity}
              </span>
            </div>

            <p>
              <strong>Reason:</strong>{" "}
              {finding.reason}
            </p>

            <p>
              <strong>Impact:</strong>{" "}
              {finding.impact}
            </p>

            <p>
              <strong>
                Recommendation:
              </strong>{" "}
              {
                finding.recommendation
              }
            </p>
          </div>
        ))
      )}
    </div>
  );
}

export default FindingList;