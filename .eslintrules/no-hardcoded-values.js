module.exports = {
  rules: {
    'no-hardcoded-values': {
      meta: {
        type: 'problem',
        docs: { description: 'disallow hardcoded hex/px values; use tokens' },
      },
      create(context) {
        return {
          Literal(node) {
            if (typeof node.value === 'string' && /#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})/.test(node.value)) {
              context.report({ node, message: 'Hardcoded color hex detected; use tokens' });
            }
            if (typeof node.value === 'string' && /\b\d+px\b/.test(node.value)) {
              context.report({ node, message: 'Hardcoded px detected; use tokens' });
            }
          }
        };
      }
    }
  }
};
