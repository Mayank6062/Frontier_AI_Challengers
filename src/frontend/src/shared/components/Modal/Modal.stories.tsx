import React from 'react';
import { StoryObj } from '@storybook/react';
import Modal from './Modal';

const meta = {
  title: 'Shared/Modal',
  component: Modal,
};

export default meta;

export const Default: StoryObj = {
  args: {
    open: true,
    children: <div>Modal body content</div>,
  },
};
