import type { StorybookConfig } from '@storybook/react-webpack5';

const config: StorybookConfig = {
  stories: ['../src/shared/components/**/*.stories.@(ts|tsx|mdx)'],
  addons: ['@storybook/addon-essentials', '@storybook/addon-a11y'],
  framework: {
    name: '@storybook/react-webpack5',
    options: {},
  },
  core: {
    builder: 'webpack5',
  },
  webpackFinal: async (config) => {
    // Ensure TypeScript files are handled by Babel with the typescript preset
    config.module = config.module || {};
    config.module.rules = config.module.rules || [];

    // Add a rule to compile story files with babel-loader + preset-typescript
    const path = require('path');
    config.module.rules.unshift({
      test: /\.stories\.(ts|tsx)$/,
      include: [path.resolve(__dirname, '../src/shared/components')],
      use: [
        {
          loader: require.resolve('babel-loader'),
          options: {
            presets: [
              [require.resolve('@babel/preset-react'), { runtime: 'automatic' }],
              require.resolve('@babel/preset-typescript'),
            ],
          },
        },
      ],
    });

    config.resolve = config.resolve || {};
    config.resolve.extensions = Array.from(
      new Set([...(config.resolve.extensions || []), '.ts', '.tsx'])
    );

    return config;
  },
};

export default config;
