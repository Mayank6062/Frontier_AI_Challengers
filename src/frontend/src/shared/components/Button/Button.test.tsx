import React from 'react';
import { render } from '@testing-library/react';
import Button from './Button';
import axe from 'axe-core';

describe('Button', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
