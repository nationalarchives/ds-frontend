/* eslint-disable */
import { dirname, resolve } from "path";
import { fileURLToPath } from "url";
import fs from "fs";
import chokidar from "chokidar";
import { build } from "vite";

const projectDirectory = dirname(fileURLToPath(import.meta.url));

const entries = {
  main: resolve(projectDirectory, "src/scripts/main.mjs"),
  analytics: resolve(projectDirectory, "src/scripts/analytics.mjs"),
  code: resolve(projectDirectory, "src/scripts/code.mjs"),
  cookies: resolve(projectDirectory, "src/scripts/cookies.mjs"),
  events: resolve(projectDirectory, "src/scripts/events.mjs"),
  education: resolve(projectDirectory, "src/scripts/education.mjs"),
  exhibition: resolve(projectDirectory, "src/scripts/exhibition.mjs"),
  footnotes: resolve(projectDirectory, "src/scripts/footnotes.mjs"),
  media: resolve(projectDirectory, "src/scripts/media.mjs"),
  offline: resolve(projectDirectory, "src/scripts/offline.mjs"),
  "record-article": resolve(projectDirectory, "src/scripts/record-article.mjs"),
  sentry: resolve(projectDirectory, "src/scripts/sentry.mjs"),
  "service-worker": resolve(projectDirectory, "src/scripts/service-worker.mjs"),
};

const outDir = resolve(projectDirectory, "app/static");
const srcDir = resolve(projectDirectory, "src");

async function buildSingleEntry(name, entryPath) {
  await build({
    configFile: false,
    build: {
      outDir,
      emptyOutDir: false,
      lib: {
        entry: entryPath,
        formats: ["es"],
        fileName: () => `${name}.min.js`,
      },
      rollupOptions: {
        external: [],
        treeshake: true,
      },
      minify: "terser",
      sourcemap: true,
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true,
          passes: 3,
          // unsafe: true,
        },
        mangle: {
          toplevel: true,
        },
        format: {
          comments: false,
        },
      },
    },
  });
}
async function runAll() {
  for (const [name, entryPath] of Object.entries(entries)) {
    await buildSingleEntry(name, entryPath);
  }
}

const isWatchMode =
  process.argv.includes("--watch") || process.argv.includes("-w");

await runAll();

if (isWatchMode) {
  console.log("\nWatching for file changes in src/...");

  const watcher = chokidar.watch(srcDir, {
    ignoreInitial: true,
    awaitWriteFinish: {
      stabilityThreshold: 100,
      pollInterval: 50,
    },
  });

  watcher.on("all", async (event, filePath) => {
    console.log(`\n[${event}] ${filePath}`);
    const entry = Object.entries(entries).find(([name, entryPath]) => {
      return filePath.startsWith(entryPath);
    });
    if (entry) {
      const [name, entryPath] = entry;
      await buildSingleEntry(name, entryPath);
    } else {
      console.log("File change not in entries, rebuilding all...");
      await runAll();
    }
  });
}
