import React from 'react';
import { render } from '@testing-library/react';
import Skeleton from './Skeleton';
import axe from 'axe-core';

describe('Skeleton', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<Skeleton />);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
