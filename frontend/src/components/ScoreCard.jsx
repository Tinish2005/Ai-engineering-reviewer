function ScoreCard({
  overall = 0,
  verdict = "UNKNOWN",
}) {
  return (
    <div className="card">
      <h2>Engineering Score</h2>

      <div className="score-number">
        {overall}
      </div>

      <div className="score-status">
        {verdict.toUpperCase()}
      </div>
    </div>
  );
}

export default ScoreCard;