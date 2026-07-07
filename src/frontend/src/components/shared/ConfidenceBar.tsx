import React from 'react';

interface ConfidenceBarProps {
  value: number; // 0-1
  label?: string;
}

/**
 * ConfidenceBar - Visual representation of confidence level
 */
export const ConfidenceBar: React.FC<ConfidenceBarProps> = ({
  value,
  label,
}) => (
  <div className="confidence-bar">
    {label && <span>{label}</span>}
    <div
      className="bar"
      style={{ width: `${value * 100}%` }}
    />
  </div>
);

export default ConfidenceBar;
