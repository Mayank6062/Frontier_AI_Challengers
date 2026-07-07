import React from 'react';
import { render } from '@testing-library/react';
import ScoreHeroCard from './ScoreHeroCard';
import axe from 'axe-core';

describe('ScoreHeroCard', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<ScoreHeroCard title="A" score={75} />);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
