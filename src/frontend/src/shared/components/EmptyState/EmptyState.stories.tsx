import React from 'react';
import { StoryObj } from '@storybook/react';
import EmptyState from './EmptyState';

const meta = {
  title: 'Shared/EmptyState',
  component: EmptyState,
};

export default meta;

export const Default: StoryObj = {
  args: {
    title: 'No results',
    description: 'Try adjusting your filters',
  },
};
