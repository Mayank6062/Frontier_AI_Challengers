import React from 'react';
import { render } from '@testing-library/react';
import CitationTag from './CitationTag';
import axe from 'axe-core';

describe('CitationTag', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<CitationTag text="Docs" />);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
