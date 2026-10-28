# Reference audit status

Approved by the user at the package 03 checkpoint on 18 October 2026.
Package 08 acceptance is effective following
[PR 9 completion](https://github.com/smiggs/code-review-skill-codex/pull/9#issuecomment-6464622303). Package 09 has conditional
human acceptance subject to current-head CodeRabbit and merge gates. Package
10 has conditional human acceptance subject to current-head CodeRabbit and
merge gates. This is an audit
disposition, not a claim that all supported languages have been technically
verified. The [review contract](review-contract.md) governs all inherited advice.

## Reading the status

"Verified within scope" means the checks described in the
[audit summary](provenance.md#verification) were
performed. It does not establish compatibility with every runtime or framework.
"Retained, not technically verified" means the guide remains available as a
source of inspection prompts, with version-specific claims to be checked against
the target's official documentation. "Needs correction" identifies a known
conflict or unsupported recommendation, without inventing a broader audit.

## File disposition

| File | Status | Scope and remaining limits |
| --- | --- | --- |
| [Review contract](review-contract.md) | Approved in package 01 | Substantive terms preserved. |
| [Python](python.md) | Verified within scope | Rewritten in British English; standalone examples exercised on Python 3.10.12, version boundaries checked in official documentation. No runtime matrix or dependency-specific audit. |
| [Review practices](code-review-best-practices.md) | Verified within scope | Process and evidence rules reconciled with the contract; no organisational performance claims. |
| [Architecture](architecture-review-guide.md) | Verified within scope | Requirement-based prompts replace universal patterns, metric thresholds, and automatic severity. Target architectures still require their own evidence. |
| [Performance](performance-review-guide.md) | Verified within scope | Evidence and workload rules reconciled; selected browser, caching, and PostgreSQL claims checked in primary documentation. No framework benchmarks or universal thresholds. |
| [Security](security-review-guide.md) | Verified within scope | Scope, authority, and evidence rules reconciled; bounded authorisation and command/path guidance checked. No complete application, cryptography, or dependency audit. |
| [Common bugs](common-bugs-checklist.md) | Partially reconciled; retained, not technically verified | Python, TypeScript/React/Vue, and Rust duplicates consolidated into their guides; Go routing added. Other inherited examples remain unverified. Patterns are prompts rather than defect evidence. |
| [React](react.md) | Checked within package 08 scope; accepted via PR 9 | React/React DOM 19.3.1 Hook, form, action, and state-identity checks passed in jsdom 30.1.3; exact Hook compiled with TypeScript 6.0.3. Query 5.105.0 source inspected and cached-data refetch error exercised. Next.js 15 remains documentation-only; no browser, hydration, or review-accuracy claim. |
| [Vue](vue.md) | Checked within package 08 scope; accepted via PR 9 | Exact composable compiled with TypeScript 6.0.3 and passed controlled request tests in Vue 3.5.44/jsdom. SFC compiled/executed with 3.4.38 and 3.5.44; no full vue-tsc, browser, hydration, general patch matrix, or review-accuracy claim. |
| [Rust](rust.md) | Checked within package 09 scope; conditional acceptance | Exact fragments compiled on Rust 1.85.0, editions 2021/2024, Tokio 1.48.0. Controlled partial I/O, cancellation, task shutdown, and valid unsafe calls passed; release mode checked. All ten harness tests also passed Miri on nightly-2025-02-20, one seed/target, edition 2021; inherited bounds defect reproduced. No sanitiser, FFI, full feature/target matrix, or review-accuracy claim. |
| [TypeScript](typescript.md) | Checked within package 08 scope; accepted via PR 9 | TypeScript 6.0.3 strict compilation and Node.js 24.22.1 runtime cases passed for the retained reader and synthetic type controls. Compiler/lint settings stay project-specific; no broad runtime matrix or review-accuracy claim. |
| [Java](java.md) | Checked within package 10 scope; conditional acceptance | Exact guide examples compiled on JDK 21.0.13; the pattern-switch example needed the JDK 17 preview flag and the virtual-thread example was rejected on both JDK 17 targets (JDK 19+ API boundary). Hibernate 6.4.10.Final with H2 2.2.224 checked eager-collection statement counts, inner versus left fetch-join membership, in-memory pagination, and proxy-safe identifier equality. Spring 6.1.14 checked proxy mode, self-invocation, package-visible advice, non-routable private methods, and the readOnly hint. No Spring Boot autoconfiguration, other providers or JDK releases, or review-accuracy claim. |
| [Go](go.md) | Checked within package 09 scope; conditional acceptance | Exact worker example compiled on Go 1.22.12 with boundary, cancellation, closure, shutdown, and race checks; module 1.21/1.22 loop comparisons passed. No broad toolchain/platform matrix, performance benchmark, or review-accuracy claim. |
| [C](c.md) | Retained, not technically verified | Language mode, implementation, ownership, and undefined-behaviour examples need verification. |
| [C++](cpp.md) | Retained, not technically verified | Standard-version, lifetime, library, and tooling assumptions need verification. |
| [CSS, Less, and Sass](css-less-sass.md) | Retained, not technically verified; policy feedback corrected | Removed count-based blocking feedback and automatic checklist priority. Browser and preprocessor examples remain unverified. |
| [Qt](qt.md) | Retained, not technically verified | Qt version, threading, ownership, and signal examples need a technical pass. |

This status file records its own scope rather than claiming an independent audit
of itself. No language guide was removed or renamed. The entry point retains
selective routing to each guide; consult the status when deciding what needs
additional verification.

## Consolidation and deferred work

The Python section in the common-bug checklist now routes to `python.md` instead
of duplicating examples and string-concatenation advice. Its TypeScript, React,
and Vue sections now route to their audited guides. Package 09 consolidates Rust
and adds Go routing; other language sections
retain their original role as pattern prompts. The four topic/process
guides were shortened because their automatic severity, unqualified code recipes,
and review-time or metric gates conflicted with the approved contract. Their paths
and review scope remain available; only the Python language guide was rewritten
by package 03.

Package 08 rewrites TypeScript, React, and Vue in British English, with source
checks recorded in `plans/evidence/08-typescript-react-and-vue.md` in the source
checkout. Scoped compilation and framework checks, fixture sensitivity, and
remaining limits are recorded in `plans/evidence/08-executable-verification.md`.
Package 08 human acceptance became effective after the PR 9 review and merge
gates passed. Any separately agreed model review evaluation remains outside
that technical acceptance.
Package 09 rewrites Go and Rust in British English, with exact-example checks,
source records, fixture sensitivity, and conditional human acceptance recorded in
`plans/evidence/09-go-and-rust.md` in the source checkout.
Package 10 rewrites Java in British English with the same method: exact-example
compile checks on the declared JDK targets, Hibernate/H2 and Spring Framework
fixture checks, and prepared review fixtures with answer keys under
`plans/evidence/10-executable-checks/` in the source checkout. The Java section
in the common-bug checklist now routes to `java.md`; other inherited checklist
sections retain their original role as pattern prompts. The other three non-Python
language guides are unchanged. The CSS guide has only
scoped English policy corrections; its technical examples retain their original content.
The rewritten guides and audit evidence are English only. These limits are
intentional deferrals for human review, not successful multilingual validation.
Helper correctness remains package 04 work and independent review-behaviour
evaluation remains package 05 work. Installation and publishing remain separate.
