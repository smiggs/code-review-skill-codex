# Package 10 executable checks

This development-only harness verifies the claims retained in
`reference/java.md`. It extracts every Java guide code fence verbatim and
compiles each as a standalone file on the declared JDK targets, runs JUnit
contract checks that exercise those extracted bytes plus JDK, Hibernate,
and Spring contracts, and runs fixture-sensitivity checks for the prepared
review fixtures. It does not invoke a model reviewer.

## Reproduction

Use Linux/x86_64, Python 3.10+, JDK 21.0.13 and JDK 17.0.21 (Temurin), and
Maven 3.9.9. This audit executed them from disposable caches under
`~/.cache/cr-plan-10/`; the Maven local repository also lives outside the
checkout, so no repository CI change is required. Setting
`JDK21_HOME` and `JDK17_HOME` is enough for `extract.py`; the Maven runs
need `JAVA_HOME` at 21. To fetch once and then stay offline, run the Maven
commands with `-Dmaven.repo.local=...` and `-o` after one online run.

From the repository root:

```bash
JDK21_HOME=/path/to/jdk-21.0.13+9 JDK17_HOME=/path/to/jdk-17.0.21+9 \
  python3 plans/evidence/10-executable-checks/extract.py
JAVA_HOME=/path/to/jdk-21.0.13+9 mvn test \
  -f plans/evidence/10-executable-checks/pom.xml \
  -Dmaven.repo.local=/path/to/local/repo
python3 plans/evidence/10-executable-checks/verify.py
```

`extract.py` publishes every ```java fence from `reference/java.md` into
ignored `.generated/guide-src` and compiles three targets per block:
JDK 21 `--release 21`, JDK 21 `--release 17` (both without preview), and
JDK 17 `--enable-preview --release 17`. Every block must compile on target
21. A block failing plain 17 either compiles with 17 preview flags
(language-preview boundary) or fails with an API-absence marker recorded in
the identity file (JDK 19+ API boundary: `ExecutorService` is `AutoCloseable`
from JDK 19 and `newVirtualThreadPerTaskExecutor` reports "Since: 21"; the
guide states both). Identities land in `.generated/results/`.

The Maven module pins JUnit 5.10.2, Hibernate ORM 6.4.10.Final, H2 2.2.224,
and Spring Framework 6.1.14 (Spring Boot 3.2.12's dependency management
lists Hibernate 6.4.10.Final and H2 2.2.224 for the 3.2 line). Statement
counts come from a Hibernate `StatementInspector`; the Spring checks run
plain Spring Framework contexts (not Spring Boot autoconfiguration).

JUnit sources under `src/test/java/invalid/example/package10`:

- `GuideExamplesTest` loads the compiled, unmodified guide bytes and checks
  their behaviour (record validation, pattern switch branches, text block
  output, reverse close order with suppression, executor drain/interrupt,
  virtual-thread execution, `compute()` totals, shared formatter).
- `ExecutorContractTest` checks `Future.cancel(true)` interruption and that
  `close()` waits for a submitted task.
- `ConcurrentMapContractTest` holds the two-record contract under a forced
  interleave for the guide's `compute()` example, and demonstrates that a
  check-then-act variant under the same two-record contract loses exactly
  one record.
- `JpaFetchTest` measures eager-collection statement counts (N+1), inner
  versus left join fetch membership, single-query counts, in-memory
  pagination (no LIMIT pushed to H2), identifier equality across an
  uninitialised proxy, and lazy access outside a session.
- `SpringProxyTransactionTest` checks the proxy mode (JDK dynamic versus
  CGLIB), self-invocation bypass, package-visible method advice under
  Spring 6 defaults, the non-routable private method, the `readOnly`
  hint on the transaction status, and clean unannotated beans.

`verify.py` copies the module into temporary directories, swaps in either
the [fixture head/base pair](fixtures/README.md), and runs the matching
contract test with a 180-second bound. Each head must fail for the expected
reason; each base must pass. Fresh outputs write to `.generated/results/`;
copy a deliberate run into `results/` when preparing evidence.

## Baselines and limits

Baselines: Linux/x86_64, Temurin JDKs 17.0.21 and 21.0.13, Maven 3.9.9,
Hibernate ORM 6.4.10.Final, H2 2.2.224, Spring Framework 6.1.14, JUnit
5.10.2, surefire 3.2.5, compiler plugin 3.13.0. All dependency versions are
pinned in `pom.xml`. Deliberate test failures, stack traces from sensitivity
runs, and recorded Hibernate warnings belong to the passing runs that
 exhibit them. No production database, container runtime, Spring Boot
autoconfiguration, JDK 25+ behaviour, performance benchmark, or full
feature/toolchain matrix is covered. Compile checks show compiler
acceptance at the pinned versions only; they do not prove runtime
behaviour beyond what the tests exercise. Passing these checks does not
establish review accuracy or authorise any evaluation claim. This technical
audit does not complete package 05 or authorise a release; see
[fixtures](fixtures/README.md) for the separately agreed evaluation
boundary.
