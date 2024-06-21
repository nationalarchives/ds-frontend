const path = require("path");

module.exports = {
  entry: {
    main: "./src/scripts/main.js",
    analytics: "./src/scripts/analytics.js",
    article: "./src/scripts/article.js",
    cookies: "./src/scripts/cookies.js",
    search: "./src/scripts/search.js",
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
  devtool: "source-map",
};
