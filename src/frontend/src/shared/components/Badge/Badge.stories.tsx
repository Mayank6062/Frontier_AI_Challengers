import React from 'react';
import { StoryObj } from '@storybook/react';
import Badge from './Badge';

const meta = {
  title: 'Shared/Badge',
  component: Badge,
};

export default meta;

export const Default: StoryObj = {
  args: {
    children: 'New',
  },
};
