import React from 'react';
import { render } from '@testing-library/react';
import Badge from './Badge';
import axe from 'axe-core';

describe('Badge', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<Badge>New</Badge>);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
