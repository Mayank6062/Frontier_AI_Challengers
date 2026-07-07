import React from 'react';
import { render } from '@testing-library/react';
import Card from './Card';
import axe from 'axe-core';

describe('Card', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<Card>Content</Card>);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
