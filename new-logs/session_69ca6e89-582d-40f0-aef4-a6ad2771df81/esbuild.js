const esbuild = require('esbuild');
const chokidar = require('chokidar');
const { join } = require('path');

const watch = process.argv.includes('--watch');

const buildOptions = {
  entryPoints: ['src/index.ts'],
  bundle: true,
  outfile: 'dist/index.js',
  platform: 'node',
  format: 'cjs',
  sourcemap: true,
  target: 'node20',
  external: ['@types/node', 'fs', 'path', 'os', 'child_process', 'http', 'https', 'crypto'], // Externalize Node.js built-ins and types
};

async function build() {
  try {
    await esbuild.build(buildOptions);
    console.log('Build successful!');
  } catch (err) {
    console.error('Build failed:', err);
  }
}

async function run() {
  if (watch) {
    console.log('Watching for changes...');
    await build(); // Initial build

    const watcher = chokidar.watch('src/**/*.ts', {
      ignored: /node_modules/, // Ignore node_modules
      persistent: true,
    });

    watcher.on('change', async (filePath) => {
      console.log(`File changed: ${filePath}`);
      await build();
    });

    watcher.on('add', async (filePath) => {
        console.log(`File added: ${filePath}`);
        await build();
    });

    watcher.on('unlink', async (filePath) => {
        console.log(`File removed: ${filePath}`);
        await build();
    });

    // Keep the process running
    process.stdin.resume();

  } else {
    await build();
    process.exit(0); // Exit after build if not watching
  }
}

run().catch(err => {
  console.error('Error during esbuild process:', err);
  process.exit(1);
});
