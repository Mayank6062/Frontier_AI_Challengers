import React from 'react';
import { StoryObj } from '@storybook/react';
import CommandPalette from './CommandPalette';

const meta = {
  title: 'Shared/CommandPalette',
  component: CommandPalette,
};

export default meta;

export const Default: StoryObj = {
  args: {
    commands: [{ id: 'c1', label: 'One' }, { id: 'c2', label: 'Two' }],
  },
};
