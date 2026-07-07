import React from 'react';
import { StoryObj } from '@storybook/react';
import Icon from './Icon';

const meta = {
  title: 'Shared/Icon',
  component: Icon,
};

export default meta;

export const Default: StoryObj = {
  args: {
    name: 'star',
    size: 24,
  },
};
