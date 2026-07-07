import React from 'react';
import { StoryObj } from '@storybook/react';
import ScoreHeroCard from './ScoreHeroCard';

const meta = {
  title: 'Shared/ScoreHeroCard',
  component: ScoreHeroCard,
};

export default meta;

export const Default: StoryObj = {
  args: {
    title: 'Architecture Score',
    score: 86,
  },
};
