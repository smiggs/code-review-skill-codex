# Prepared Java fixtures

These synthetic, distributable fixtures supply one defective `head` and a
clean `base` each; the head/base differences are single-line edits. The
fixtures need the package 10 Maven module and the contract tests in
`src/test/java/invalid/example/package10/fixturesupport` to compile and
exercise them. `verify.py` proves that the contract tests reject each head
for the expected reason and accept each base; this is sensitivity evidence
only, not a measurement of model detection or accuracy.

- [jpa-membership](jpa-membership/): `ParentReader.readStaleParents` must
  return every requested catalogue user, including users with no related
  orders. The base issues `LEFT JOIN FETCH`; the head silently drops
  child-less users with an inner `JOIN FETCH`.
- [failure-observability](failure-observability/): `BatchRunner.collectResults`
  must publish an outcome for every nightly job, including failures. The base
  records each task's failure in the returned list; the head swallows the
  exception inside the task so the caller never sees it.

For a future independent review, provide only the selected head/base diff,
the necessary module metadata (Maven module, JDK 21, Hibernate ORM 6.4.10.Final,
H2 2.2.224, Spring Framework 6.1.14 where relevant), and the target
requirement above. The [answer keys](answer-key.md), contract-test sources,
sensitivity logs, and audit narrative must be withheld from the reviewer.
Before any model runs: agree review prompts, isolation, scoring, severity
expectations, and acceptance criteria. No such evaluation has been run or
accepted for package 10.
