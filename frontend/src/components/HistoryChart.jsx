import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function HistoryChart({ history = [] }) {
  if (!history.length) return null;

  return (
    <div className="card">
      <h2>📈 Review History</h2>

      <ResponsiveContainer
        width="100%"
        height={300}
      >
        <LineChart data={history}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="id" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="score"
            stroke="#2563eb"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default HistoryChart;