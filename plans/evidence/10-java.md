# Package 10: Java audit evidence

Date: 28 October 2026. Technical audit candidate prepared at the user's
request under [the plan](../10-java.md); no human checkpoint has yet
reviewed it. This work does not reopen package 05, authorise publication,
or establish review accuracy for the changed guide. The [package 03
method](03-python-and-reference-quality.md) and the shared audit
requirements in [the plans README](../README.md) govern scope.

## Candidate and changes

Work began on `main` at `118253c` (the package 09 merge). The working
candidate is identified by the [manifest](10-executable-checks/results/candidate-manifest.json)
built the same way as
package 09's: SHA-256 over sorted `path NUL bytes NUL` records. It covers
the guide, checklist, disposition, provenance, plan documents, harness,
fixtures, and result records; it excludes this narrative, the manifest
itself, and generated sources, caches, and toolchains. The human
checkpoint should name the manifest's combined digest or an exact committed
revision.

`reference/java.md` was rewritten in British English using the Google
documentation variant of the house style. Its existing path, core selective
routing, skill identity, MIT attribution, and the code-review contract
links remain. A Java routing section was added to the common-bug checklist;
no other checklist section changed. Reference disposition and provenance
now describe this scoped candidate. The inherited guide's own checklists
(style preferences) were removed; route-and-contract prompts replace
them.

| Area | Correction and resulting contract |
| --- | --- |
| Switch patterns | The inherited `case Integer i: // Java 16+` claim misstated the boundary: pattern matching for switch is final in JDK 21 (JEP 441) after previews 17–20 (JEPs 406/420/427/433). `instanceof` patterns are JDK 16. Compiler evidence: the retained switch fence compiles plainly on `--release 21`; on JDK 17.0.21 it needs `--enable-preview`. |
| Version boundaries | Records final in 16 (JEP 395), switch expressions 14 (JEP 361), text blocks 15 (JEP 378), `String.formatted` 15, `Stream.toList()` 16, virtual threads final 21 after previews 19/20 (JEP 425/436), `ExecutorService` `AutoCloseable` from 19 with `close()` on JDK 21 waiting indefinitely (no timeout of its own, interrupt escalates to `shutdownNow`). The fence with `newVirtualThreadPerTaskExecutor` compiles only on the 21 target (API boundary recorded). |
| Resource closure and interruption | Reverse-order close on failure and suppressed close failures tracked to JLS §14.20.3 and exercised with a runnable failing-close example; executor ownership now separates `shutdown`/`awaitTermination`/`shutdownNow` with the javadoc's best-effort interruption caveat; tests exercise interruption delivery and a `close()` wait. |
| Shared mutable state | The inherited blanket rules became per-method contracts: `ConcurrentHashMap` retrievals do not lock and per-method operations are atomic; a two-record contract distinguishes the guide's `compute()` example from a check-then-act variant which loses exactly one record under forced interleaving; `SimpleDateFormat`/`DateTimeFormatter` claims use exact javadoc quotes; the HashMap death-loop claim is qualified (JDK-7027300 fixed in 8; lost updates and best-effort fail-fast remain) with shared-map locking as a clean control. |
| Spring transactions | Proxy mode, self-invocation, visibility, and the readOnly hint now match the Spring 6.x contracts: JDK-dynamic versus CGLIB proxy selection; 6.0's default allowing protected/package-visible transactional methods for class-based proxies; interface proxies limited to public interface methods; private methods not routable (demonstrated via proxy class member lookup); `readOnly` as a javadoc-quoted hint. Layering choices, DI style, and virtual-thread property coverage are preferences until a measured consequence, not defects. |
| JPA persistence | EAGER collections issue one eager select per parent on entity queries (1 + N measured); `JOIN FETCH` inner joins drop child-less parents while `LEFT JOIN FETCH` preserves them (all three parents present, empty collections not null), both demonstrated with recorded statement counts; Hibernate 6.4 applies `setMaxResults` on a collection fetch in memory without pushing LIMIT to SQL (the 6.4 log id for the warning is HHH90003004, replacing the inherited 5.x-era HHH000104); entity equality over proxies: the conventional identifier getter does not initialise an uninitialised proxy, while the proxy's own `hashCode()` does (observed); `@Data`'s all-field equals/hashCode is suspect only when lazy fields are reachable from comparison. |
| Preferences removed | Streams, Optional shapes, DI style, Lombok, test frameworks, virtual threads, and layering arrangements no longer stand alone as defect evidence; each retains its underlying contract instead. |

## Sources and version boundaries

Primary sources were accessed on 28 October 2026:

| Claims checked | Primary sources |
| --- | --- |
| Language feature boundaries and pinning | [JEP 441](https://openjdk.org/jeps/441), [JEP 406](https://openjdk.org/jeps/406), [JEP 433](https://openjdk.org/jeps/433), [JEP 395](https://openjdk.org/jeps/395), [JEP 361](https://openjdk.org/jeps/361), [JEP 378](https://openjdk.org/jeps/378), [JEP 425](https://openjdk.org/jeps/425), [JEP 436](https://openjdk.org/jeps/436), [JEP 444](https://openjdk.org/jeps/444), [JEP 491](https://openjdk.org/jeps/491). |
| JDK documentation | [ExecutorService](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ExecutorService.html), [Executors](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Executors.html), [Future](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Future.html), [ConcurrentHashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html), [HashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html), [SimpleDateFormat](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/text/SimpleDateFormat.html), [DateTimeFormatter](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/format/DateTimeFormatter.html), [Stream](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Stream.html), [String (JDK 15)](https://docs.oracle.com/en/java/javase/15/docs/api/java.base/java/lang/String.html), [JLS §14.20.3](https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.20.3), [JDK 17 language changes](https://docs.oracle.com/en/java/javase/17/language/java-language-changes.html), [JDK-7027300](https://bugs.openjdk.org/browse/JDK-7027300). |
| Spring Framework and Boot (6.2/6.2.19 docs quoting the 6.x contracts; Boot wiki) | [Declarative transactions](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html), [proxying](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html), [@Transactional javadoc](https://docs.spring.io/spring-framework/docs/6.2.19/javadoc-api/org/springframework/transaction/annotation/Transactional.html), [HibernateJpaDialect javadoc](https://docs.spring.io/spring-framework/docs/6.2.19/javadoc-api/org/springframework/orm/jpa/vendor/HibernateJpaDialect.html), [ProblemDetail javadoc](https://docs.spring.io/spring-framework/docs/6.2.19/javadoc-api/org/springframework/http/ProblemDetail.html), [scheduling reference](https://docs.spring.io/spring-framework/reference/6.2/integration/scheduling.html), [@EnableAsync javadoc](https://docs.spring.io/spring-framework/docs/6.2.19/javadoc-api/org/springframework/scheduling/annotation/EnableAsync.html), [Boot 3.0 release notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Release-Notes), [Boot 3.2 release notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.2-Release-Notes), [Boot 3.2.12 dependency versions](https://docs.spring.io/spring-boot/docs/3.2.12/reference/html/dependency-versions.html). |
| JPA, Hibernate, Lombok | [Jakarta Persistence 3.1](https://jakarta.ee/specifications/persistence/3.1/jakarta-persistence-spec-3.1.html) (fetch joins §4.4.5.3, EAGER/LAZY), [Hibernate ORM 6.4 user guide](https://docs.jboss.org/hibernate/orm/6.4/userguide/html_single/Hibernate_User_Guide.html) and [6.4 javadoc](https://docs.jboss.org/hibernate/orm/6.4/javadocs/org/hibernate/proxy/AbstractLazyInitializer.html), [QueryLogging (HHH90003004)](https://github.com/hibernate/hibernate-orm/blob/6.4/hibernate-core/src/main/java/org/hibernate/query/QueryLogging.java), [Lombok @Data](https://projectlombok.org/features/Data). |

The current Spring reference site serves Framework 7.0 pages, so the 6.x
sentences were taken from the versioned `6.2` paths; Hibernate's rolling
user-guide page reports 6.4 content; JDK pages are the 21-line documents
except where a versioned variant (String 15) is stated. No claim is made
for other documents' wording between these access date versions.
`getClass().hashCode()`-style recipes are treated as secondary blog
recommendations and the guide instead cites Hibernate's user guide
(identifier equality with a constant `hashCode`, natural keys).

## Executable verification

The [harness](10-executable-checks/README.md) records portable commands,
extraction, fixtures, and locked dependency versions. Baselines are
Linux/x86_64 with Temurin JDK 21.0.13 and 17.0.21 (fetched with the
Adoptium-reported SHA-256 checksums), Maven 3.9.9, Hibernate ORM
6.4.10.Final, H2 2.2.224, Spring Framework 6.1.14, and JUnit 5.10.2. All
dependency versions are pinned; the Maven repository lives outside the
checkout. Initial toolchain work struck the `/tmp` disk quota again; the
fix (disposable caches under the home filesystem) was part of the user's
carried-over guidance, and everything was re-fetched into
`~/.cache/cr-plan-10`. Neither incident counts as a behavioural result.

| Check | Observed result |
| --- | --- |
| Guide extraction and compile matrix | 8 ```java fences extracted; all compile on `--release 21` without preview flags; TypeDescriber (pattern switch) needs `--enable-preview` on JDK 17 as recorded; VirtualExecutorOwnership is a JDK 19+ API boundary recorded with the missing-symbol error. [Identities](10-executable-checks/results/source-identities.json) and [extraction output](10-executable-checks/results/extract.txt). |
| Full Maven suite | 28 tests: 26 executed, failures 0 and errors 0, 2 gated fixture-contract tests skip in the plain suite and run only under `verify.py`. [Output](10-executable-checks/results/full-suite.txt). |
| Guide example behaviour | Record validation, switch branches including `case null`, text block output, reverse close order with suppression, executor drain and interruption, virtual-thread execution, `compute()` exactness under concurrency, and shared formatter correctness all pass over the exact extracted bytes. |
| JDK contracts | `Future.cancel(true)` interrupt delivery and `close()`'s wait for a running task pass with bounded waits. |
| Shared mutable state | Forced-interleave contract: the `compute()` guide example keeps both records; the check-then-act variant loses exactly one. |
| Hibernate/H2 | EAGER `@OneToMany` costs 1 + N statements; `JOIN FETCH` runs 1 statement and drops the child-less parent; `LEFT JOIN FETCH` runs 1 statement and preserves all three parents (no duplicate rows for the 3-user sample); with `setMaxResults(2)` no LIMIT appears in H2 SQL (in-memory application) and the first two parents are returned; identifier equality over an uninitialised `getReference` proxy holds without initialisation through the conventional getter, while the proxy's `hashCode()` initialises it (recorded observation); lazy owner access outside the session raises `LazyInitializationException`. [Output](10-executable-checks/results/full-suite.txt). |
| Spring Framework 6.1.14 | Public interface method advised through a JDK proxy; self-invocation bypasses the proxy (no transaction); package-visible method advised through CGLIB under 6.x defaults; the private method is not routable on the proxy class and runs without a transaction through self-invocation; `readOnly` visible on the transaction status; unannotated bean and concrete-interface validations pass as clean controls. |
| Fixture sensitivity | Both defective heads rejected for the expected contract reasons; both clean bases passed. [Summary](10-executable-checks/results/sensitivity.txt) with per-run [head](10-executable-checks/results/fixture-jpa-membership-head.txt)/[base](10-executable-checks/results/fixture-jpa-membership-base.txt) and [head](10-executable-checks/results/fixture-failure-observability-head.txt)/[base](10-executable-checks/results/fixture-failure-observability-base.txt) outputs. |

The checks are synthetic: H2 in-memory databases, a driver-only Spring
context (no Spring Boot autoconfiguration, no container web stack), no
production data, no browser or network I/O, and no other JDK or provider
releases. Statement-count and membership assertions describe the audited
versions, not a universal matrix. Skipped gated tests are disclosed rather
than hidden; deliberate assertion failures in sensitivity outputs document
where the defective heads break. No model-reviewed report exists.

## Documentation checks and human decision

The [validation log](10-executable-checks/results/validation.txt) records:
`git diff --check` and `git diff --stat`; 18 passing repository
helper/validator tests; 13 passing package 03 examples; structural
validation with all relative links resolving within the package;
skill-creator quick validation ("Skill is valid!", run from a preserved
copy of the system skill-creator because the live install ships no script);
house-style lint of the ten changed or rewritten Markdown files. The lint
reports zero errors in all new prose with three allow-listed verbatim-quote
words (`synchronized`, `parameterized`, `initialize`); it still reports two
inherited checklist lines and two title warnings in sections packages 03–09
deliberately retained unchanged. These checks establish mechanical
consistency only; they do not establish useful review behaviour.

Human decision: the user supplied conditional acceptance on 28 October
2026, recorded in the [approval record](10-pr-approval.md) and effective
after a completed clean CodeRabbit review of the current head, resolved
threads, dispositions and replies for review-body findings, passing required
checks and approvals, and a GitHub merge commit guarded by that exact head.
The reviewer should still check the corrections, declared versions, retained
scope, translation limits, and the evaluation boundary against the manifest
digest or an exact committed revision.

The Chinese installation and contribution documents need no shared-behaviour
change: this work changes reference guidance only. The rewritten guide and
evidence are English only, with no bilingual technical validation. Any model
review evaluation requires separately agreed prompts, withheld answer keys,
criteria, and raw reports; the [prepared fixtures](10-executable-checks/fixtures/README.md)
and answer keys stay unpublished until that agreement. Accuracy claims,
package 05 completion, and release authorisation are out of scope here.
