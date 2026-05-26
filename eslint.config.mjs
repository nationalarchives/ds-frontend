import tnaEslintConfig from "@nationalarchives/eslint-config";
import { defineConfig, globalIgnores } from "eslint/config";

export default defineConfig([
  ...tnaEslintConfig,
  {
    rules: {
      "capitalized-comments": "off",
      "no-magic-numbers": "off",
      "no-new": "off",
      "no-ternary": "warn",
      "one-var": "off",
      "sort-imports": ["error", { ignoreDeclarationSort: true }],
      "sort-keys": "off",
      "sort-vars": "off",
    },
  },
  globalIgnores(["app/static/**/*", "webpack.config.js"]),
]);
