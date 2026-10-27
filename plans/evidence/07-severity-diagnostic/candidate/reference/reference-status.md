# Reference audit status

Approved by the user at the package 03 checkpoint on 18 October 2026. This is an audit
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
| [Common bugs](common-bugs-checklist.md) | Partially reconciled; retained, not technically verified | Python duplicates consolidated into the Python guide; inherited framework examples remain unverified. Patterns are prompts rather than defect evidence. |
| [React](react.md) | Retained, not technically verified | React and query-library version assumptions and examples need a technical pass. |
| [Vue](vue.md) | Retained, not technically verified | Version-sensitive reactivity and lifecycle examples need a technical pass. |
| [Rust](rust.md) | Retained, not technically verified | Ownership, unsafe, runtime, and cancellation examples need a technical pass. |
| [TypeScript](typescript.md) | Retained, not technically verified | Compiler and lint recommendations must defer to project versions and configuration. |
| [Java](java.md) | Retained, not technically verified | JDK, Spring, persistence, and concurrency claims need version-specific verification. |
| [Go](go.md) | Retained, not technically verified | Runtime, generics, error, and concurrency examples need a technical pass. |
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
of duplicating examples and string-concatenation advice. Its other language
sections retain their original role as pattern prompts. The four topic/process
guides were shortened because their automatic severity, unqualified code recipes,
and review-time or metric gates conflicted with the approved contract. Their paths
and review scope remain available; no language guide was rewritten by that change.

Nine non-Python language guides are unchanged. The CSS guide has only scoped
English policy corrections; its technical examples retain their original content.
The rewritten guides and audit evidence are English only. These limits are
intentional deferrals for human review, not successful multilingual validation.
Helper correctness remains package 04 work and independent review-behaviour
evaluation remains package 05 work. Installation and publishing remain separate.
