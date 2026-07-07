import React from "react";

export const Icon: React.FC<{ name: string; size?: number | string }> = ({ name, size = "var(--og2-components-icons-size-md)" }) => {
  const style: any = { fill: "currentColor", verticalAlign: "middle" };
  return (
    <svg
      width={size}
      height={size}
      aria-hidden
      focusable={false}
      style={style}
    >
      <rect width="100%" height="100%" />
    </svg>
  );
};

export default Icon;
