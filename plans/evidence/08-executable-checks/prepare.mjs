import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import ts from 'typescript';
import * as compiler35 from '@vue/compiler-sfc';
import * as compiler34 from 'compiler34';

const root = new URL('../../../', import.meta.url);
const out = new URL('./.generated/', import.meta.url);
await mkdir(out, { recursive: true });
const identities = {};
async function blocks(path, language) {
  const source = await readFile(new URL(path, root), 'utf8');
  identities[path] = createHash('sha256').update(source).digest('hex');
  return [...source.matchAll(/^```([^\n]+)\n([\s\S]*?)^```/gm)]
    .filter(match => match[1] === language).map(match => match[2]);
}
const [reader] = await blocks('reference/typescript.md', 'typescript');
const [react] = await blocks('reference/react.md', 'tsx');
const [vue] = await blocks('reference/vue.md', 'typescript');
const [sfc] = await blocks('reference/vue.md', 'vue');
if (![reader, react, vue, sfc].every(Boolean)) throw new Error('Missing guide example');
await writeFile(new URL('reader.ts', out), reader + '\nexport { readValue };\n');
await writeFile(new URL('react.tsx', out), react);
await writeFile(new URL('vue.ts', out), vue);
await writeFile(new URL('props.vue', out), sfc);
for (const [label, compiler, runtime] of [
  ['35', compiler35, 'vue'], ['34', compiler34, 'vue34'],
]) {
  const { descriptor, errors } = compiler.parse(sfc, { filename: 'props.vue' });
  if (errors.length) throw new Error(errors.join('\n'));
  const script = compiler.compileScript(descriptor, {
    id: 'package-08-props', inlineTemplate: true,
  });
  const js = ts.transpileModule(script.content, {
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext },
    reportDiagnostics: true,
  });
  if (js.diagnostics?.length) throw new Error('SFC transpilation diagnostics');
  await writeFile(new URL(`props${label}.js`, out),
    js.outputText.replaceAll('from "vue"', `from "${runtime}"`)
      .replaceAll("from 'vue'", `from '${runtime}'`));
}
await writeFile(new URL('type-controls.ts', out),
  await readFile(new URL('./type-controls.ts', import.meta.url), 'utf8'));
for (const [caseId, filename, output] of [
  ['case-01', 'reader.ts', 'reader-defect.ts'],
  ['case-02', 'react.tsx', 'react-defect.tsx'],
  ['case-03', 'vue.ts', 'vue-defect.ts'],
  ['case-01', 'reader.ts', 'reader-control.ts'],
  ['case-02', 'react.tsx', 'react-control.tsx'],
  ['case-03', 'vue.ts', 'vue-control.ts'],
]) {
  await writeFile(new URL(output, out),
    await readFile(new URL(`./fixtures/${caseId}/${output.includes('control') ? 'base' : 'head'}/${filename}`, import.meta.url), 'utf8'));
}
const config = {
  compilerOptions: {
    target: 'ES2022', module: 'NodeNext', moduleResolution: 'NodeNext',
    strict: true, noUncheckedIndexedAccess: true, jsx: 'react-jsx',
    lib: ['ES2022', 'DOM'], noEmitOnError: true, types: ['react', 'react-dom'],
  },
  files: ['reader.ts', 'react.tsx', 'vue.ts', 'type-controls.ts',
    'reader-defect.ts', 'react-defect.tsx', 'vue-defect.ts',
    'reader-control.ts', 'react-control.tsx', 'vue-control.ts'],
};
await writeFile(new URL('tsconfig.json', out), JSON.stringify(config, null, 2));
const result = spawnSync(process.execPath,
  [fileURLToPath(new URL('./node_modules/typescript/bin/tsc', import.meta.url)),
    '-p', fileURLToPath(new URL('tsconfig.json', out))], { encoding: 'utf8' });
process.stdout.write(result.stdout || '');
process.stderr.write(result.stderr || '');
if (result.status !== 0) process.exit(result.status ?? 1);
await writeFile(new URL('identities.json', out), JSON.stringify(identities, null, 2));
console.log('Compiled exact TypeScript/React/Vue guide blocks and both SFC compiler modes.');
