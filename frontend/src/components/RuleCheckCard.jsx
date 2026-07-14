function RuleCheckCard({
  title,
  rules_passed,
  rules_failed,
  results = [],
}) {
  return (
    <div className="card">
      <h2>{title}</h2>

      <div className="rule-summary">
        <div className="pass-box">
          ✅ Passed:
          <h2>{rules_passed}</h2>
        </div>

        <div className="fail-box">
          ❌ Failed:
          <h2>{rules_failed}</h2>
        </div>
      </div>

      {results.map((rule, index) => (
        <div
          key={index}
          className="rule-item"
        >
          <span>
            {rule.status === "pass"
              ? "✅"
              : "❌"}
          </span>

          <strong>
            {rule.rule}
          </strong>

          <span>
            Status:
            {rule.status}
          </span>
        </div>
      ))}
    </div>
  );
}

export default RuleCheckCard;