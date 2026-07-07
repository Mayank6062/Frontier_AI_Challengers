import React from 'react';
import { render } from '@testing-library/react';
import Icon from './Icon';
import axe from 'axe-core';

describe('Icon', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<Icon name="star" />);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
