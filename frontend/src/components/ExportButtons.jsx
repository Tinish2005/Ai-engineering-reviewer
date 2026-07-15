function ExportButtons() {
  const API = "http://127.0.0.1:5000";
  const latestReviewId = 33;

  const handleExport = (format) => {
    window.open(`${API}/export/${format}/${latestReviewId}`, "_blank", "noopener,noreferrer");
  };

  return (
    <div style={{ display: "flex", gap: "12px", marginTop: "24px", flexWrap: "wrap" }}>
      <button className="export-btn json-btn" onClick={() => handleExport("json")}>
        📄 Export JSON
      </button>
      <button className="export-btn md-btn" onClick={() => handleExport("markdown")}>
        📝 Export Markdown
      </button>
      <button className="export-btn pdf-btn" onClick={() => handleExport("pdf")}>
        📕 Export PDF
      </button>
    </div>
  );
}

export default ExportButtons;