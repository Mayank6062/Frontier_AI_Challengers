import React from 'react';

interface ScoreHeroCardProps {
  title: string;
  score: number; // 0-100
  details?: React.ReactNode;
}

/**
 * ScoreHeroCard - Large score display card
 */
export const ScoreHeroCard: React.FC<ScoreHeroCardProps> = ({
  title,
  score,
  details,
}) => (
  <div className="score-hero-card">
    <h3>{title}</h3>
    <div className="score">{score}</div>
    {details && <div className="details">{details}</div>}
  </div>
);

export default ScoreHeroCard;
