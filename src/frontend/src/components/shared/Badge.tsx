import React from 'react';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  children: React.ReactNode;
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'error';
}

/**
 * Badge - Small label component
 */
export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  className,
  ...props
}) => (
  <span className={`badge badge-${variant} ${className || ''}`} {...props}>
    {children}
  </span>
);

export default Badge;
