import React from 'react';
import { StoryObj } from '@storybook/react';
import Card from './Card';

const meta = {
  title: 'Shared/Card',
  component: Card,
};

export default meta;

export const Default: StoryObj = {
  args: {
    children: <div>Card content</div>,
  },
};
