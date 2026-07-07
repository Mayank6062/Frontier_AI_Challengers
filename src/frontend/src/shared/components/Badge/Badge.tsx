import React from "react";

export const Badge: React.FC<{ children?: React.ReactNode }> = ({ children }) => (
  <span
    role="status"
      style={{
        background: 'var(--og2-semantic-success-light, var(--og2-green_40))',
        color: 'var(--og2-semantic-text-primary-light, var(--og2-colors_gray_90))',
        padding: 'var(--og2-components-spacing-space-1) var(--og2-components-spacing-space-2)',
        borderRadius: 'var(--og2-components-radii-radius-1)',
        fontSize: 'var(--og2-components-typography-size-sm)',
      }}
  >
    {children}
  </span>
);

export default Badge;
