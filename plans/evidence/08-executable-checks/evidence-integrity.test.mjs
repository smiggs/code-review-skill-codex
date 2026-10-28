import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cp, mkdtemp, readFile, readdir, rm, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { gunzipSync } from 'node:zlib';

const source = fileURLToPath(new URL('./', import.meta.url));
test('routine sensitivity runs preserve recorded evidence and write fresh generated results', async () => {
  const workspace = await mkdtemp(join(tmpdir(), 'package-08-evidence-'));
  try {
    for (const name of ['package.json', 'sensitivity.mjs', 'checks.test.mjs', '.generated', 'results']) {
      await cp(join(source, name), join(workspace, name), { recursive: true });
    }
    await symlink(join(source, 'node_modules'), join(workspace, 'node_modules'), 'dir');
    const recorded = new Map();
    for (const name of await readdir(join(workspace, 'results'))) {
      recorded.set(name, await readFile(join(workspace, 'results', name)));
    }
    const generated = join(workspace, '.generated', 'results');
    await rm(generated, { recursive: true, force: true });
    const result = spawnSync(process.execPath, [join(workspace, 'sensitivity.mjs')], {
      cwd: workspace, encoding: 'utf8',
    });
    assert.equal(result.status, 0, (result.stdout ?? '') + (result.stderr ?? ''));
    for (const [name, before] of recorded) {
      assert.deepEqual(await readFile(join(workspace, 'results', name)), before,
        `Routine execution changed recorded evidence: ${name}`);
    }
    for (const name of ['reader', 'react', 'vue']) {
      const red = gunzipSync(await readFile(join(generated, `red-${name}.txt.gz`))).toString();
      const green = await readFile(join(generated, `green-${name}.txt`), 'utf8');
      assert.match(red, /not ok/);
      assert.match(green, /# fail 0/);
    }
  } finally {
    await rm(workspace, { recursive: true, force: true });
  }
});
