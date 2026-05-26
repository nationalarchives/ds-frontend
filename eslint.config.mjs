import tnaEslintConfig from "@nationalarchives/eslint-config";
import { defineConfig, globalIgnores } from "eslint/config";

export default defineConfig([
  ...tnaEslintConfig,
  globalIgnores(["app/static/**/*", "webpack.config.js"]),
]);
