function ScoreCard({
  overall = 0,
  verdict = "UNKNOWN",
  categories = [],
}) {
  const getColor = (score) => {
    if (score >= 85) return "#22c55e";
    if (score >= 70) return "#eab308";
    return "#ef4444";
  };

  return (
    <div className="card">
      <h2>Engineering Score</h2>

      <div
        style={{
          display: "flex",
          gap: "30px",
          flexWrap: "wrap",
          alignItems: "center",
        }}
      >
        <div
          style={{
            width: "180px",
            height: "180px",
            borderRadius: "50%",
            border: `12px solid ${getColor(overall)}`,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <h1
            style={{
              margin: 0,
              fontSize: "48px",
            }}
          >
            {overall}
          </h1>

          <p
            style={{
              margin: 0,
              color: "#9ca3af",
            }}
          >
            /100
          </p>
        </div>

        <div style={{ flex: 1 }}>
          <h3
            style={{
              color: getColor(overall),
            }}
          >
            {verdict.toUpperCase()}
          </h3>

          {categories.map(
            (category, index) => (
              <div
                key={index}
                style={{
                  marginBottom: "12px",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent:
                      "space-between",
                  }}
                >
                  <span>
                    {category.name}
                  </span>

                  <span>
                    {category.score}
                  </span>
                </div>

                <div
                  style={{
                    background:
                      "#374151",
                    height: "8px",
                    borderRadius:
                      "999px",
                  }}
                >
                  <div
                    style={{
                      width: `${category.score}%`,
                      height: "8px",
                      borderRadius:
                        "999px",
                      background:
                        getColor(
                          category.score
                        ),
                    }}
                  />
                </div>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}

export default ScoreCard;
