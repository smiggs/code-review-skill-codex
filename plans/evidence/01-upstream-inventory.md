# Package 01 upstream baseline and inventory

Recorded on 18 October 2026 from local Git objects. This inventory describes the
inherited baseline; it makes no claim about the latest remote revision.

## Provenance

- Adapted upstream: [NefelibataBIGR/code-review-skill-codex](https://github.com/NefelibataBIGR/code-review-skill-codex).
- Baseline: `dcd254772fc253143889b6ab0184f31296482426`, the local
  `refs/remotes/upstream/main` and parent of the initial planning commit.
- Baseline subject: `Update title in README.zh-CN.md`; author: Nefelibata.
- Fork source before package 01: `a327c0fe8e1e9bb95b6b1602dad04a7f6ee83bd9`.
  Its only additions relative to the baseline are `AGENTS.md` and eight plan files.
- Earlier source credited by both baseline READMEs at line 5:
  [awesome-skills/code-review-skill](https://github.com/awesome-skills/code-review-skill).
  No commit, copied-file mapping, or separate licence for that earlier source is
  recorded in this checkout. Its provenance has not been independently audited.
- Preserved licence: [LICENSE](../../LICENSE), MIT, with the exact notice
  `Copyright (c) 2026 Nefelibata`. Original attribution remains in both READMEs.

Evidence commands (read-only):

```bash
git remote -v
git rev-parse refs/remotes/upstream/main
git show --no-patch --format=fuller dcd254772fc253143889b6ab0184f31296482426
git ls-tree -r --name-only dcd254772fc253143889b6ab0184f31296482426
git diff --name-status dcd254772fc253143889b6ab0184f31296482426 a327c0fe8e1e9bb95b6b1602dad04a7f6ee83bd9
```

## File inventory

All 27 tracked baseline files follow. No guide is removed, renamed, translated,
or technically endorsed by this inventory.

| Baseline path | Role | Inbound route or mention in the baseline |
| --- | --- | --- |
| `.gitignore` | Ignore rules | Git; no document link |
| `CONTRIBUTING.md` | English contribution guidance | English README and both contribution language switches |
| `CONTRIBUTING.zh-CN.md` | Chinese contribution guidance | Chinese README and both contribution language switches |
| `LICENSE` | MIT licence and attribution | No internal Markdown link |
| `README.md` | English usage and installation | Both README language switches |
| `README.zh-CN.md` | Chinese usage and installation | Both README language switches |
| `SKILL.md` | Discovery and core review entry point | Both READMEs link it; both contribution guides mention it |
| `agents/openai.yaml` | UI metadata | Both READMEs and contribution guides mention it |
| `assets/pr-review-template.md` | PR report template | SKILL.md; both README layout trees |
| `assets/review-checklist.md` | Review checklist | SKILL.md; both README layout trees |
| `reference/architecture-review-guide.md` | Topic guide | SKILL.md; both README layout trees |
| `reference/c.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/code-review-best-practices.md` | Topic guide | SKILL.md; both README layout trees |
| `reference/common-bugs-checklist.md` | Topic guide | SKILL.md; both README layout trees |
| `reference/cpp.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/css-less-sass.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/go.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/java.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/performance-review-guide.md` | Topic guide | SKILL.md; both README layout trees |
| `reference/python.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/qt.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/react.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/rust.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/security-review-guide.md` | Topic guide | SKILL.md; both README layout trees |
| `reference/typescript.md` | Language/framework guide | SKILL.md; both README layout trees |
| `reference/vue.md` | Language/framework guide | SKILL.md; both README layout trees |
| `scripts/pr-analyzer.py` | Heuristic diff-statistics helper | Both README layout trees; no entry-point Markdown link |

Both contribution guides mention `reference/*.md`, `assets/*`, and `scripts/*`
as contribution categories. Both READMEs list every baseline reference and asset
by filename in their layout trees. Those are text mentions, not Markdown links.
The UI metadata has no file dependencies; the helper has no local-document links.

## Inbound Markdown link inventory

Every internal Markdown link occurrence follows, including self-links and
contents anchors. Source lines refer to the baseline. Fenced code examples are
excluded. External URLs in topic guides are outbound reading, not internal entry
routes. External inbound links cannot be inventoried from this checkout.

### Links between files

| Source and line | Destination |
| --- | --- |
| `CONTRIBUTING.md:1` | `./CONTRIBUTING.md` |
| `CONTRIBUTING.md:1` | `./CONTRIBUTING.zh-CN.md` |
| `CONTRIBUTING.zh-CN.md:1` | `./CONTRIBUTING.md` |
| `CONTRIBUTING.zh-CN.md:1` | `./CONTRIBUTING.zh-CN.md` |
| `README.md:1` | `./README.md` |
| `README.md:1` | `./README.zh-CN.md` |
| `README.md:39` | `./SKILL.md` |
| `README.md:152` | `./CONTRIBUTING.md` |
| `README.zh-CN.md:1` | `./README.md` |
| `README.zh-CN.md:1` | `./README.zh-CN.md` |
| `README.zh-CN.md:39` | `./SKILL.md` |
| `README.zh-CN.md:152` | `./CONTRIBUTING.zh-CN.md` |
| `SKILL.md:97` | `reference/architecture-review-guide.md` |
| `SKILL.md:100` | `reference/performance-review-guide.md` |
| `SKILL.md:127` | `reference/security-review-guide.md` |
| `SKILL.md:170` | `reference/react.md` |
| `SKILL.md:171` | `reference/vue.md` |
| `SKILL.md:172` | `reference/rust.md` |
| `SKILL.md:173` | `reference/typescript.md` |
| `SKILL.md:174` | `reference/python.md` |
| `SKILL.md:175` | `reference/java.md` |
| `SKILL.md:176` | `reference/go.md` |
| `SKILL.md:177` | `reference/c.md` |
| `SKILL.md:178` | `reference/cpp.md` |
| `SKILL.md:179` | `reference/css-less-sass.md` |
| `SKILL.md:180` | `reference/qt.md` |
| `SKILL.md:184` | `reference/architecture-review-guide.md` |
| `SKILL.md:185` | `reference/performance-review-guide.md` |
| `SKILL.md:186` | `reference/common-bugs-checklist.md` |
| `SKILL.md:187` | `reference/security-review-guide.md` |
| `SKILL.md:188` | `reference/code-review-best-practices.md` |
| `SKILL.md:189` | `assets/pr-review-template.md` |
| `SKILL.md:190` | `assets/review-checklist.md` |

### Links within a file

| Source and line | Destination anchor |
| --- | --- |
| `reference/c.md:7` | `#pointer-and-buffer-safety` |
| `reference/c.md:8` | `#ownership-and-resource-management` |
| `reference/c.md:9` | `#undefined-behavior-pitfalls` |
| `reference/c.md:10` | `#integer-types-and-overflow` |
| `reference/c.md:11` | `#error-handling` |
| `reference/c.md:12` | `#concurrency` |
| `reference/c.md:13` | `#macros-and-preprocessor` |
| `reference/c.md:14` | `#api-design-and-const` |
| `reference/c.md:15` | `#tooling-and-build-checks` |
| `reference/c.md:16` | `#review-checklist` |
| `reference/cpp.md:7` | `#ownership-and-raii` |
| `reference/cpp.md:8` | `#lifetime-and-references` |
| `reference/cpp.md:9` | `#copy-and-move-semantics` |
| `reference/cpp.md:10` | `#const-correctness-and-api-design` |
| `reference/cpp.md:11` | `#error-handling-and-exception-safety` |
| `reference/cpp.md:12` | `#concurrency` |
| `reference/cpp.md:13` | `#performance-and-allocation` |
| `reference/cpp.md:14` | `#templates-and-type-safety` |
| `reference/cpp.md:15` | `#tooling-and-build-checks` |
| `reference/cpp.md:16` | `#review-checklist` |
| `reference/java.md:7` | `#现代-java-特性-1721` |
| `reference/java.md:8` | `#stream-api--optional` |
| `reference/java.md:9` | `#spring-boot-最佳实践` |
| `reference/java.md:10` | `#jpa-与-数据库性能` |
| `reference/java.md:11` | `#并发与虚拟线程` |
| `reference/java.md:12` | `#lombok-使用规范` |
| `reference/java.md:13` | `#异常处理` |
| `reference/java.md:14` | `#测试规范` |
| `reference/java.md:15` | `#review-checklist` |
| `reference/performance-review-guide.md:7` | `#前端性能-core-web-vitals` |
| `reference/performance-review-guide.md:8` | `#javascript-性能` |
| `reference/performance-review-guide.md:9` | `#内存管理` |
| `reference/performance-review-guide.md:10` | `#数据库性能` |
| `reference/performance-review-guide.md:11` | `#api-性能` |
| `reference/performance-review-guide.md:12` | `#算法复杂度` |
| `reference/performance-review-guide.md:13` | `#性能审查清单` |
| `reference/python.md:7` | `#类型注解` |
| `reference/python.md:8` | `#异步编程` |
| `reference/python.md:9` | `#异常处理` |
| `reference/python.md:10` | `#常见陷阱` |
| `reference/python.md:11` | `#测试最佳实践` |
| `reference/python.md:12` | `#性能优化` |
| `reference/python.md:13` | `#代码风格` |
| `reference/python.md:14` | `#review-checklist` |
| `reference/qt.md:7` | `#object-model--memory-management` |
| `reference/qt.md:8` | `#signals--slots` |
| `reference/qt.md:9` | `#containers--strings` |
| `reference/qt.md:10` | `#threads--concurrency` |
| `reference/qt.md:11` | `#gui--widgets` |
| `reference/qt.md:12` | `#meta-object-system` |
| `reference/qt.md:13` | `#review-checklist` |
| `reference/react.md:7` | `#基础-hooks-规则` |
| `reference/react.md:8` | `#useeffect-模式` |
| `reference/react.md:9` | `#usememo--usecallback` |
| `reference/react.md:10` | `#组件设计` |
| `reference/react.md:11` | `#error-boundaries--suspense` |
| `reference/react.md:12` | `#server-components-rsc` |
| `reference/react.md:13` | `#react-19-actions--forms` |
| `reference/react.md:14` | `#suspense--streaming-ssr` |
| `reference/react.md:15` | `#tanstack-query-v5` |
| `reference/react.md:16` | `#review-checklists` |
| `reference/rust.md:7` | `#所有权与借用` |
| `reference/rust.md:8` | `#unsafe-代码审查最关键` |
| `reference/rust.md:9` | `#异步代码` |
| `reference/rust.md:10` | `#取消安全性` |
| `reference/rust.md:11` | `#spawn-vs-await` |
| `reference/rust.md:12` | `#错误处理` |
| `reference/rust.md:13` | `#性能` |
| `reference/rust.md:14` | `#trait-设计` |
| `reference/rust.md:15` | `#rust-review-checklist` |
| `reference/typescript.md:7` | `#类型安全基础` |
| `reference/typescript.md:8` | `#泛型模式` |
| `reference/typescript.md:9` | `#高级类型` |
| `reference/typescript.md:10` | `#strict-模式配置` |
| `reference/typescript.md:11` | `#异步处理` |
| `reference/typescript.md:12` | `#不可变性` |
| `reference/typescript.md:13` | `#eslint-规则` |
| `reference/typescript.md:14` | `#review-checklist` |
| `reference/vue.md:7` | `#响应性系统` |
| `reference/vue.md:8` | `#props--emits` |
| `reference/vue.md:9` | `#vue-35-新特性` |
| `reference/vue.md:10` | `#watchers` |
| `reference/vue.md:11` | `#模板最佳实践` |
| `reference/vue.md:12` | `#composables` |
| `reference/vue.md:13` | `#性能优化` |
| `reference/vue.md:14` | `#review-checklist` |

## Adaptation boundaries

Package 01 adds the proposed [review contract](../../reference/review-contract.md)
and [checkpoint evidence](01-foundation-and-review-contract.md). The package plan,
plan index, and both READMEs link these records. `AGENTS.md` records fork policy.
The contract will be routed from `SKILL.md` in package 02 when its workflow and
both templates are aligned. Package 01 does not implement that migration.

Known divergence for package 02 includes compulsory praise, question phrasing,
minute budgets, the large-PR split request, and approval language. Guides need
reconciliation in package 03. This inventory records routes rather than technical
or behavioural validation of inherited advice or helper behaviour.
