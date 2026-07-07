module.exports = function (api) {
  api && typeof api.cache === 'function' && api.cache(true);

  return {
    presets: [
      ['@babel/preset-env', { targets: '> 0.25%, not dead' }],
      ['@babel/preset-react', { runtime: 'automatic' }],
      '@babel/preset-typescript',
    ],
  };
};
