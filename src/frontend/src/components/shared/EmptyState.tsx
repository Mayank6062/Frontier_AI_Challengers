import React from 'react';

interface EmptyStateProps {
  title: string;
  message?: string;
  action?: React.ReactNode;
}

/**
 * EmptyState - Display when no content available
 */
export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  message,
  action,
}) => (
  <div className="empty-state">
    <h3>{title}</h3>
    {message && <p>{message}</p>}
    {action && <div>{action}</div>}
  </div>
);

export default EmptyState;
