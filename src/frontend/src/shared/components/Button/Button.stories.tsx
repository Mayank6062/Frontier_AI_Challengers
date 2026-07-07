import React from 'react';
import { StoryObj } from '@storybook/react';
import Button from './Button';

const meta = {
  title: 'Shared/Button',
  component: Button,
};

export default meta;

export const Primary: StoryObj = {
  args: {
    children: 'Primary Button',
    onClick: () => alert('clicked'),
  },
};
