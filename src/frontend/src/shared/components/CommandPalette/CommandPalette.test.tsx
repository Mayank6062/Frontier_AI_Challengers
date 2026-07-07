import React from 'react';
import { render } from '@testing-library/react';
import CommandPalette from './CommandPalette';
import axe from 'axe-core';

describe('CommandPalette', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<CommandPalette commands={[{ id: 'c1', label: 'One' }]} />);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
