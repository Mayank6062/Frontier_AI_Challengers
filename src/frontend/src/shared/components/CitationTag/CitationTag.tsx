import React from "react";

export const CitationTag: React.FC<{ text: string }> = ({ text }) => (
  <span style={{ color: 'var(--og2-semantic-text-secondary-light, var(--og2-colors_gray_70))', fontSize: 'var(--og2-components-typography-size-sm)' }}>{text}</span>
);

export default CitationTag;
