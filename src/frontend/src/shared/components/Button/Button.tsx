import React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export const Button = ({ children, ...rest }: ButtonProps) => {
  return (
    <button
      {...rest}
      style={{
        background: 'var(--og2-semantic-interactive-primary-light, var(--og2-blue_40))',
        color: 'var(--og2-semantic-text-primary-light, var(--og2-colors_gray_90))',
        borderRadius: 'var(--og2-components-radii-radius-1)',
        padding: 'var(--og2-components-spacing-space-2) var(--og2-components-spacing-space-3)',
        border: 'none',
      }}
      aria-pressed={rest["aria-pressed"]}
    >
      {children}
    </button>
  );
};

export default Button;
