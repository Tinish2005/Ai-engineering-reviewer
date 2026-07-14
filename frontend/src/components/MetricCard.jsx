import {
  FileCode,
  FunctionSquare,
  MessageSquare,
  Layers,
} from "lucide-react";

function MetricCard({ title, data }) {
  const metrics = [
    {
      label: "Total Lines",
      value: data?.total_lines ?? 0,
      icon: <FileCode size={18} />,
    },
    {
      label: "Code Lines",
      value: data?.code_lines ?? 0,
      icon: <FileCode size={18} />,
    },
    {
      label: "Functions",
      value: data?.function_count ?? 0,
      icon: <FunctionSquare size={18} />,
    },
    {
      label: "Classes",
      value: data?.class_count ?? 0,
      icon: <Layers size={18} />,
    },
    {
      label: "Comments %",
      value: data?.comment_ratio_pct ?? 0,
      icon: <MessageSquare size={18} />,
    },
  ];

  return (
    <div
      style={{
        background: "#111827",
        border: "1px solid #1f2937",
        borderRadius: "16px",
        padding: "20px",
        marginBottom: "20px",
      }}
    >
      <h2
        style={{
          color: "white",
          marginBottom: "20px",
        }}
      >
        {title}
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(180px,1fr))",
          gap: "16px",
        }}
      >
        {metrics.map((metric) => (
          <div
            key={metric.label}
            style={{
              background: "#1f2937",
              borderRadius: "12px",
              padding: "16px",
            }}
          >
            <div
              style={{
                color: "#60a5fa",
                marginBottom: "10px",
              }}
            >
              {metric.icon}
            </div>

            <div
              style={{
                color: "#9ca3af",
                fontSize: "14px",
              }}
            >
              {metric.label}
            </div>

            <div
              style={{
                color: "white",
                fontSize: "28px",
                fontWeight: "bold",
              }}
            >
              {metric.value}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MetricCard;