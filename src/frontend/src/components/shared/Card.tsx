import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

/**
 * Card - Container component for grouped content
 */
export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, children, ...props }, ref) => (
    <div ref={ref} className={`card ${className || ''}`} {...props}>
      {children}
    </div>
  )
);

Card.displayName = 'Card';

export default Card;
