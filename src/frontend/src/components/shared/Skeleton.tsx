import React from 'react';

interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  count?: number;
}

/**
 * Skeleton - Loading placeholder component
 */
export const Skeleton: React.FC<SkeletonProps> = ({
  width = '100%',
  height = '20px',
  count = 1,
}) => (
  <>
    {Array(count)
      .fill(0)
      .map((_, i) => (
        <div
          key={i}
          className="skeleton"
          style={{ width, height, marginBottom: '8px' }}
        />
      ))}
  </>
);

export default Skeleton;
