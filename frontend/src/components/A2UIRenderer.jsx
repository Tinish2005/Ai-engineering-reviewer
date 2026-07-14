import ScoreCard from "./ScoreCard";
import MetricCard from "./MetricCard";
import ComplexityCard from "./ComplexityCard";
import FindingList from "./FindingList";
import RuleCheckCard from "./RuleCheckCard";
import AISummary from "./AISummary";

const registry = {
  score_card: ScoreCard,
  metric_card: MetricCard,
  complexity_card: ComplexityCard,
  finding_list: FindingList,
  rule_check_card: RuleCheckCard,
  ai_summary: AISummary,
};

function A2UIRenderer({ components = [] }) {
  return (
    <>
      {components.map((component, index) => {
        const Component = registry[component.type];

        if (!Component) {
          console.warn(
            "Unknown component type:",
            component.type
          );
          return (
            <div
              key={index}
              style={{
                background: "#1e293b",
                color: "white",
                padding: "16px",
                borderRadius: "12px",
                marginBottom: "16px",
              }}
            >
              Unknown component:
              {component.type}
            </div>
          );
        }

        return (
          <Component
            key={index}
            {...component}
          />
        );
      })}
    </>
  );
}

export default A2UIRenderer;
