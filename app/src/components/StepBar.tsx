import "./StepBar.css";

const steps = ["Search", "Itinerary", "Passengers", "Seats", "Terms", "Review"];

export default function StepBar({ active }: { active: number }) {
  return (
    <nav aria-label="Reservation progress">
      <ol className="stepbar reservation-stepbar">
        {steps.map((step, index) => {
          const isActive = index === active;
          const isComplete = index < active;

          return (
            <li
              key={step}
              className={`reservation-step${isActive ? " is-active" : ""}${isComplete ? " is-complete" : ""}`}
              aria-current={isActive ? "step" : undefined}
            >
              <span className="step-indicator" aria-hidden="true">
                {isComplete ? "✓" : index + 1}
              </span>
              <span className="step-label">{step}</span>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
