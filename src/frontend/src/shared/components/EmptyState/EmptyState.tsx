import React from "react";

export const EmptyState: React.FC<{ title?: string; description?: string }> = ({ title, description }) => (
  <div style={{ textAlign: 'center', padding: 'var(--og2-components-spacing-space-5)' }}>
    <h3 style={{ color: "var(--og2-semantic-text-primary-light)" }}>{title}</h3>
    <p style={{ color: "var(--og2-semantic-text-secondary-light)" }}>{description}</p>
  </div>
);

export default EmptyState;
