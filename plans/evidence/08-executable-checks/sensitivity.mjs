import { spawnSync } from 'node:child_process';
import { writeFile } from 'node:fs/promises';
import { gzipSync } from 'node:zlib';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
const testFile = fileURLToPath(new URL('./checks.test.mjs', import.meta.url));
for (const [label, variable, module, pattern, expected] of [
  ['reader', 'P08_READER', './.generated/reader-defect.js', 'value reader accepts', 'Missing expected exception'],
  ['react', 'P08_REACT', './.generated/react-defect.js', 'React: latest completion wins with abortAware=false', 'not ok'],
  ['vue', 'P08_VUE', './.generated/vue-defect.js', 'Vue: getter input obeys', 'not ok'],
]) {
  const result = spawnSync(process.execPath, ['--test', '--test-isolation=none',
    '--test-concurrency=1', '--test-reporter=tap', `--test-name-pattern=${pattern}`, testFile], {
    encoding: 'utf8', env: { ...process.env, [variable]: module },
  });
  const output = (result.stdout ?? '') + (result.stderr ?? '');
  await writeFile(new URL(`./results/red-${label}.txt.gz`, import.meta.url), gzipSync(output));
  assert.equal(result.status, 1, `${label}: defective fixture must fail its behavioural check`);
  assert.ok(output.includes(expected), `${label}: expected assertion failure was not observed`);
  const green = spawnSync(process.execPath, ['--test', '--test-isolation=none',
    '--test-concurrency=1', '--test-reporter=tap', `--test-name-pattern=${pattern}`, testFile], {
    encoding: 'utf8', env: { ...process.env, [variable]: module.replace('defect', 'control') },
  });
  await writeFile(new URL(`./results/green-${label}.txt`, import.meta.url),
    (green.stdout ?? '') + (green.stderr ?? ''));
  assert.equal(green.status, 0, `${label}: clean control must pass`);
  console.log(`${label}: defect rejected and clean control accepted by behavioural assertions`);
}
