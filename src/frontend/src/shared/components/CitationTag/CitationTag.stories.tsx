import React from 'react';
import { StoryObj } from '@storybook/react';
import CitationTag from './CitationTag';

const meta = {
  title: 'Shared/CitationTag',
  component: CitationTag,
};

export default meta;

export const Default: StoryObj = {
  args: {
    text: 'Citation example',
  },
};
