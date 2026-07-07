import React from 'react';
import { render } from '@testing-library/react';
import Modal from './Modal';
import axe from 'axe-core';

describe('Modal', () => {
  it('renders and is accessible', async () => {
    const { container } = render(<Modal open> Hello </Modal>);
    const results = await axe.run(container);
    expect(results.violations.length).toBe(0);
  });
});
