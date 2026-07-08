const path = require('path');

// Bundles the Lordicon custom element + lottie-web player into a single
// self-contained script that the Quarto extension injects into HTML output.
// `mode: 'production'` enables Terser minification automatically.
module.exports = {
  mode: 'production',
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, '_extensions/lordicon/assets/js'),
    filename: 'bundle.js',
  },
  // The bundle is dominated by lottie-web; its size is inherent, not a
  // code-splitting problem, so silence the performance advisories.
  performance: { hints: false },
};
