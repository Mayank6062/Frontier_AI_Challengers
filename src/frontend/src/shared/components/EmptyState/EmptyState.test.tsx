import React from 'react';
import { render } from '@testing-library/react';
import EmptyState from './EmptyState';
import axe from 'axe-core';

describe('EmptyState', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<EmptyState title="Nope" description="Try again" />);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
