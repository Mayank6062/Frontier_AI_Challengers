import React from 'react';
import { render } from '@testing-library/react';
import ConfidenceBar from './ConfidenceBar';
import axe from 'axe-core';

describe('ConfidenceBar', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<ConfidenceBar value={0.5} />);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
