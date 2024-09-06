const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
  entry: {
    main: "./src/scripts/main.js",
    analytics: "./src/scripts/analytics.js",
    article: "./src/scripts/article.js",
    cookies: "./src/scripts/cookies.js",
    media: "./src/scripts/media.js",
    offline: "./src/scripts/offline.js",
    "record-article": "./src/scripts/record-article.js",
    sentry: "./src/scripts/sentry.js",
    "service-worker": "./src/scripts/service-worker.js",
    sidebar: "./src/scripts/sidebar.js",
  },
  mode: "production",
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
    ],
  },
  output: {
    path: path.resolve(__dirname, "app/static"),
    filename: "[name].min.js",
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        extractComments: false,
      }),
    ],
  },
  devtool: "source-map",
};
