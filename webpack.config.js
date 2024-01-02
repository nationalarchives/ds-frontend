const path = require("path");

module.exports = {
  entry: {
    app: "./src/scripts/app.js",
    article: "./src/scripts/article.js",
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
