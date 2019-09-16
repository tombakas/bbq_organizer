const path = require('path');

module.exports = {
  module: {
    rules: [
      {
        test: /\.s[ac]ss$/i,
        use: [
          'style-loader',
          'css-loader',
          'sass-loader',
        ],
      },
    ],
  },
  entry: './bbq_organizer/static_dev/js/index.js',
  resolve: {
    modules: [path.resolve(__dirname, "app"), "node_modules"],
  },
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'bbq_organizer/static/js')
  }
};
