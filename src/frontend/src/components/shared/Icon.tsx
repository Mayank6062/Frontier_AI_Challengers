import React from 'react';

interface IconProps extends React.SVGAttributes<SVGSVGElement> {
  name: string;
}

/**
 * Icon - SVG icon component
 */
export const Icon: React.FC<IconProps> = ({ name, ...props }) => (
  <svg className={`icon icon-${name}`} {...props} />
);

export default Icon;
