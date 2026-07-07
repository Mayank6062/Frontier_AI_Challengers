import React from "react";

export const Skeleton: React.FC<{ width?: string; height?: string }> = ({ width = "100%", height = "1em" }) => {
  const prefersReduced = typeof window !== "undefined" && window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const style: any = {
    background: "linear-gradient(90deg, var(--og2-semantic-bg-surface-light, var(--og2-colors_gray_10)), var(--og2-semantic-bg-primary-light, var(--og2-colors_gray_0)))",
    width,
    height,
    borderRadius: "var(--og2-components-radii-radius-1)",
  };
  if (!prefersReduced) {
    style.animation = "og2-skeleton-shimmer 1.4s ease-in-out infinite";
  }
  return <div aria-hidden style={style} />;
};

export default Skeleton;
