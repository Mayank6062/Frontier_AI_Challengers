import React from 'react';

interface CitationTagProps {
  source: string;
  confidence?: number;
}

/**
 * CitationTag - Displays citation source and confidence
 */
export const CitationTag: React.FC<CitationTagProps> = ({
  source,
  confidence = 1,
}) => (
  <span className="citation-tag" title={`Confidence: ${Math.round(confidence * 100)}%`}>
    {source}
  </span>
);

export default CitationTag;
