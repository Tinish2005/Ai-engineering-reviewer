function ComplexityCard({
  title,
  verdict,
  cyclomatic_max,
  cognitive_max,
}) {
  return (
    <div className="card">
      <h2>{title}</h2>

      <div className="metrics-grid">
        <div className="metric-box">
          <p>Cyclomatic Complexity</p>
          <h3>{cyclomatic_max}</h3>
        </div>

        <div className="metric-box">
          <p>Cognitive Complexity</p>
          <h3>{cognitive_max}</h3>
        </div>

        <div className="metric-box">
          <p>Verdict</p>
          <h3>{verdict}</h3>
        </div>
      </div>
    </div>
  );
}

export default ComplexityCard;