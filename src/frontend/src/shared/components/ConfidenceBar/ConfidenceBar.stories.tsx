import React from 'react';
import { StoryObj } from '@storybook/react';
import ConfidenceBar from './ConfidenceBar';

const meta = {
  title: 'Shared/ConfidenceBar',
  component: ConfidenceBar,
};

export default meta;

export const Default: StoryObj = {
  args: {
    value: 0.72,
  },
};
