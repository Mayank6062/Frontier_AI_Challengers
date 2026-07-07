import React from 'react';
import { ThemeProvider } from '../src/shared/theme/ThemeProvider';
import '../src/shared/theme/tokens.css';

export const decorators = [
  (Story: any) => (
    <ThemeProvider>
      <div style={{ padding: 16 }}>
        <Story />
      </div>
    </ThemeProvider>
  ),
];

export const parameters = {
  actions: { argTypesRegex: '^on.*' },
  controls: { expanded: true },
  a11y: { element: '#root' },
};
