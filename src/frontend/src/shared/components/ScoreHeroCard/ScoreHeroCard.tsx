import React from "react";

export const ScoreHeroCard: React.FC<{ title: string; score: number }> = ({ title, score }) => {
  return (
    <div style={{ padding: 'var(--og2-components-spacing-space-4)', background: 'var(--og2-semantic-bg-surface-light)', borderRadius: 'var(--og2-components-radii-radius-2)' }}>
      <h3 style={{ margin: 0, color: "var(--og2-semantic-text-primary-light)" }}>{title}</h3>
        <div style={{ fontSize: 'var(--og2-components-typography-hero-size)', color: 'var(--og2-semantic-interactive-primary-light)' }}>{score}</div>
    </div>
  );
};

export default ScoreHeroCard;
