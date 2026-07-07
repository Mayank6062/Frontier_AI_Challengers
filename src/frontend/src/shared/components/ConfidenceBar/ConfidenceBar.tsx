import React from "react";

export const ConfidenceBar: React.FC<{ value: number }> = ({ value }) => {
  const raw = typeof value === 'number' ? value : 0;
  const normalized = raw > 0 && raw <= 1 ? raw * 100 : raw;
  const pct = Math.max(0, Math.min(100, normalized));
  return (
    <div
      role="progressbar"
      aria-label="Confidence"
      aria-valuenow={Math.round(pct)}
      aria-valuemin={0}
      aria-valuemax={100}
      style={{ background: 'var(--og2-semantic-bg-surface-light)', borderRadius: 'var(--og2-components-radii-radius-1)', height: 'var(--og2-components-confidencebar-height)' }}
    >
      <div style={{ width: `${pct}%`, height: '100%', background: 'var(--og2-semantic-success-light)' }} />
    </div>
  );
};

export default ConfidenceBar;
