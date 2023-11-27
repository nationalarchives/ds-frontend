const path = require("path");

module.exports = {
  entry: "./src/scripts/app.js",
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
    filename: "app.js",
  },
  devtool: "source-map",
};
