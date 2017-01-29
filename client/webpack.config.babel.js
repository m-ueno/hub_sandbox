import path from 'path';
import webpack from 'webpack';

const js = {
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    // new webpack.NoErrorsPlugin(),
  ],
  entry: [
    // 'webpack-hot-middleware/client', // WebpackDevServer host and port
    'webpack-dev-server/client?http://0.0.0.0:3000', // WebpackDevServer host and port
    'webpack/hot/only-dev-server', // "only" prevents reload on syntax errors
    './index.jsx',
  ],
  output: {
    path: path.join(__dirname, 'dist'),
    publicPath: '',
    filename: 'bundle.js',
  },
  devServer: {
    contentBase: './dist',
    hot: true,
    inline: true,
    host: "0.0.0.0",
    port: 3000,
    historyApiFallback: true,
  },
  devtool: 'cheap-module-eval-source-map',
  module: {
    preLoaders: [
      {
        test: /\.jsx?$/,
        loader: 'eslint',
        exclude: path.resolve('node_modules'),
      },
    ],
    loaders: [
      {
        test: /\.jsx?$/,
        loaders: ['react-hot', 'babel'],
        exclude: path.resolve('node_modules'),
      }
    ],
  },
};

export default js;
