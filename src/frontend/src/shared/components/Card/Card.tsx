import React from "react";

export const Card: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  return (
    <div
      style={{
        background: "var(--og2-semantic-bg-surface-light, var(--og2-colors_gray_10))",
        color: "var(--og2-semantic-text-primary-light, var(--og2-colors_gray_90))",
        borderRadius: 'var(--og2-components-radii-radius-2)',
        boxShadow: 'var(--og2-components-shadow-elevation-1)',
        padding: 'var(--og2-components-spacing-space-4)',
      }}
      role="group"
    >
      {children}
    </div>
  );
};

export default Card;
