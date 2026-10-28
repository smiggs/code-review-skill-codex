# Java review guide

Use this guide under the [review contract](review-contract.md). Ground findings
in reachable failure conditions, violated framework contracts, or stated project
requirements. Language-feature adoption, annotation preferences, and layering
choices alone are not defects.

## Versions and review scope

Read the declared compiler or `maven.compiler.release`/Gradle
`sourceCompatibility`/`toolchain` values, `--enable-preview` usages and preview
JEPs, `persistence.xml` or equivalent JPA configuration, Spring Boot and
Framework versions, persistence-provider and JDBC-driver versions, and CI and
test commands. The executable audit baseline is JDK 17.0.21 and JDK 21.0.13 on
Linux/x86_64, Hibernate ORM 6.4.10.Final with H2 2.2.224, and Spring Framework
6.1.14 on the Spring Boot 3.2 dependency-management line. These are
reproducibility baselines, not recommendations to migrate project versions.
Check preview and API availability against the project's own target. See the
[reference status](reference-status.md) for verification limits. Test-support,
framework, and layering choices belong to that project; missing tests alone
does not establish a defect.

## Language features and their boundaries

Below, "final in JDK N" states when a feature left preview and entered the
language; it is evidence about compiler requirements, not advice to rewrite
working code.

- [Records](https://openjdk.org/jeps/395): final in JDK 16, preview in 14 and 15.
- [Switch expressions](https://openjdk.org/jeps/361): final in JDK 14.
- [Text blocks](https://openjdk.org/jeps/378): final in JDK 15;
  `String.formatted` was added in JDK 15.
- [Pattern matching for switch](https://openjdk.org/jeps/441): final in JDK 21,
  previewed in JDK 17–20 (`case Integer i` inside a switch is not a JDK 16
  feature; only pattern matching for `instanceof` was final in
  [JDK 16](https://openjdk.org/jeps/394)). Compiling such a switch for JDK 17
  needs `--enable-preview`.
- [Virtual threads](https://openjdk.org/jeps/444): final in JDK 21, previewed in
  19 and 20; `Stream.toList()` was added in JDK 16.

A record's compact constructor can enforce declared invariants:

```java
public record UserDto(String name, int age) {
    public UserDto {
        if (age < 0) {
            throw new IllegalArgumentException("age must not be negative: " + age);
        }
    }
}
```

A switch pattern over `Object` can handle `null` explicitly; every branch needs
a descriptive consequence for the project:

```java
public class TypeDescriber {
    public static String describe(Object value) {
        return switch (value) {
            case null -> "null";
            case Integer i -> "integer %d".formatted(i);
            case String s -> "string %s".formatted(s);
            case Object o -> "unrecognised " + o.getClass().getSimpleName();
        };
    }
}
```

Text blocks preserve the writer's line structure; the closing delimiter's
indentation fixes the incidental whitespace:

```java
public class JsonTemplates {
    public static String userPayload(String name, int age) {
        return """
            {"name": "%s", "age": %d}
            """.formatted(name, age);
    }
}
```

## Optional and stream usage

`Optional` as a return type makes absence visible to callers; fields,
parameters, and collections of `Optional` usually signal a modelling problem,
and `Optional` does not implement `Serializable`. Verify what the actual
consumer does with an absent value before reporting style. `isPresent()` plus
`get()` works; functional chaining and readable multi-step pipelines are
preferences, not defect evidence.

## Resources, close contracts, and interruption

try-with-resources closes resources in **reverse order of declaration** even
when the body or an earlier `close()` fails; a `close()` failure during
exception propagation is attached to the primary exception's suppressed list
([JLS §14.20.3](https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.20.3)).
Check that ownership of each resource (opened by whom, closed by whom) is
traceable on failure paths, not merely that `close()` textually appears.

```java
import java.util.ArrayList;
import java.util.List;

public class LoggedResource implements AutoCloseable {
    private final String name;
    private final List<String> closedLog;
    private final boolean failOnClose;

    public LoggedResource(String name, List<String> closedLog, boolean failOnClose) {
        this.name = name;
        this.closedLog = closedLog;
        this.failOnClose = failOnClose;
    }

    /** Body failure propagates; both resources still close in reverse order, and
     *  the failing inner close is suppressed onto the propagated exception. */
    public static void runWithTwoResources(List<String> closedLog) {
        try (LoggedResource outer = new LoggedResource("outer", closedLog, false);
             LoggedResource inner = new LoggedResource("inner", closedLog, true)) {
            throw new IllegalStateException("body failure");
        }
    }

    @Override
    public void close() {
        closedLog.add(name);
        if (failOnClose) {
            throw new IllegalStateException("close failure of " + name);
        }
    }
}
```

An executor's receiver owns its shutdown. `shutdown()` stops admissions;
`awaitTermination` observes completion; `shutdownNow()` returns queued tasks
and "attempts to stop all actively executing tasks" [by
interruption](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ExecutorService.html)
: tasks that never observe their interrupt flag may never terminate, so
interruption handling belongs in long-running task bodies. `Future.cancel(true)`
interrupts a started task the same way. Every abandoned task needs a recorded
policy for its half-finished work.

```java
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ExecutorOwnership {
    private final ExecutorService executor;

    public ExecutorOwnership(int workerCount) {
        this.executor = Executors.newFixedThreadPool(workerCount);
    }

    /** Stops after submitted work completes. */
    public boolean drainTasks(long timeout, TimeUnit unit) throws InterruptedException {
        executor.shutdown();
        return executor.awaitTermination(timeout, unit);
    }

    /** Abandons running work; ignoring the interrupt flag risks never finishing. */
    public List<Runnable> abandonRunningTasks() {
        return executor.shutdownNow();
    }
}
```

Since [JDK 19](https://openjdk.org/jeps/425) `ExecutorService` implements
`AutoCloseable`; the JDK 21 `close()` performs an orderly shutdown and waits
for submitted tasks, calling `shutdownNow()` if interrupted. It has no timeout
of its own; a bounded shutdown needs explicit `awaitTermination` handling.
Virtual threads ([JEP 444](https://openjdk.org/jeps/444)) serve blocking,
I/O-heavy loads with many short-lived tasks; `newVirtualThreadPerTaskExecutor`
reports "Since: 21"; `newFixedThreadPool` remains valid for CPU-bound work and
is not deprecated.

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class VirtualExecutorOwnership {
    /** close() waits for the submitted task; the flag proves a virtual thread ran it. */
    public static boolean ranOnVirtualThread() throws Exception {
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            return executor.submit(() -> Thread.currentThread().isVirtual()).get();
        }
    }
}
```

A fixed thread pool is a clean control for CPU-bound work; virtual threads are
a workload-appropriate choice, not a universal default. On JDK 21, blocking
[inside `synchronized` code or native frames](https://openjdk.org/jeps/444)
pins a virtual thread to its carrier (diagnosable with
`-Djdk.tracePinnedThreads`); [JDK 24](https://openjdk.org/jeps/491) removed
that pinning for `synchronized` blocks and the diagnostic property.
A `synchronized` fast path is not a defect on either version; the measurable
difference is blocking duration under the project's actual load.

## Shared mutable state

`ConcurrentHashMap` retrievals "generally do not block" and may overlap with
updates; concurrent **single-method** use is safe, and per-method operations
such as `compute`, `merge`, and `putIfAbsent` are performed atomically
([javadoc](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html)).
A caller's compound action (read, decide, then write) remains separate
method invocations that can interleave. Check-then-act code whose decisions
must not interleave belongs in atomic map methods or external locks; the
collection's thread safety does not transfer to the caller's compound
operation. Iteration is weakly consistent, and `size`/`isEmpty` reflect
transient states unsuited to program control under concurrent updates.

```java
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class ConcurrentLedger {
    private final Map<String, Integer> totals = new ConcurrentHashMap<>();

    /** compute() applies the whole read-modify-write for a key atomically. */
    public void record(String account, int amount) {
        String key = account.toLowerCase(Locale.ROOT);
        totals.compute(key, (ignored, current) -> current == null ? amount : current + amount);
    }

    public int total(String account) {
        return totals.getOrDefault(account.toLowerCase(Locale.ROOT), 0);
    }
}
```

`SimpleDateFormat` "is not synchronized": concurrent access corrupts formatted
output, and the javadoc requires per-thread instances or external
synchronisation
([javadoc](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/text/SimpleDateFormat.html)).
`DateTimeFormatter` is [immutable and thread-safe](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/format/DateTimeFormatter.html)
and may be shared as a constant:

```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class EventFormatter {
    private static final DateTimeFormatter DAY =
        DateTimeFormatter.ofPattern("yyyy-MM-dd");

    public static String dayOf(LocalDate date) {
        return DAY.format(date);
    }
}
```

A shared `SimpleDateFormat` behind a correct
lock can be valid; what matters is the actual guard on the unguarded class.

Unsynchronised concurrent access to `HashMap` with structural modification is
unsupported behaviour
([javadoc](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html)):
it requires external synchronisation, misses updates silently, and its
fail-fast iterators detect breakage only best-effort. The JDK 7-and-earlier
resize death loop was fixed in JDK 8 ([JDK-7027300](https://bugs.openjdk.org/browse/JDK-7027300));
surviving hazards are lost updates, stale reads, and undefined table states,
not a guaranteed hang. A single-threaded or properly synchronised `HashMap` is
a clean control; `ConcurrentHashMap` is not automatically the better choice
for every map field.

## Spring transactions

`@Transactional` advice is applied by a proxy. A call arriving through the
proxy is advised; "only external method calls coming in through the proxy are
intercepted", so `this.method()` self-invocation inside the same bean bypasses
the proxy and the annotation on the invoked method then has no effect
([declarative transactions,
Spring Framework 6.x reference](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)).
Proxy mode follows the bean's shape: with `proxyTargetClass` unset,
annotation-driven transactions create JDK dynamic proxies when the target
implements an interface (routing only public interface methods) and CGLIB
subclasses otherwise; Spring recommends annotating concrete classes. Method
visibility is version-sensitive:

- "The @Transactional annotation is typically used on methods with public
  visibility. As of 6.0, protected or package-visible methods can also be made
  transactional for class-based proxies by default.";
- interface-based proxies require transactional methods to be public and
  declared in the proxied interface;
- private methods are never routed through the proxy, and self-invocation
  additionally bypasses it.

Transaction boundaries exist only where the proxy actually intercepts:
propagation, isolation, `rollbackFor` (checked exceptions default to no
rollback), and timeout are per-method contracts, and the `REQUIRED` default
joins an existing transaction rather than opening a fresh one.

`readOnly` is an optimisation **hint**: per the
[`@Transactional` javadoc](https://docs.spring.io/spring-framework/docs/6.2.19/javadoc-api/org/springframework/transaction/annotation/Transactional.html)
it "serves as a hint for the actual transaction subsystem; it will not
necessarily cause failure of write access attempts", and a manager that
cannot interpret it silently ignores the hint. Depending on the configured
transaction manager and dialect it can lower a Hibernate flush mode or set
the JDBC connection read-only
([`HibernateJpaDialect` javadoc](https://docs.spring.io/spring-framework/docs/6.2.19/javadoc-api/org/springframework/orm/jpa/vendor/HibernateJpaDialect.html)).
Check what the project's configuration actually does with the hint before
reporting a missing or wrong `readOnly`.

Transaction placement in controllers, services, or repositories is a layering
choice. A transaction spans pooled-connection hold time; its measured risk
depends on pool sizing, work inside the boundary, and load. Controller-level
transactions, missing `readOnly` hints, and missing service-layer methods are
preferences, not defects.

Since [Spring Boot 3.0](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Release-Notes),
"the @ConstructorBinding annotation is no longer required if the class has a
single parameterized constructor" (records bind through that constructor),
registered via `@EnableConfigurationProperties` or scanning. Constructor
injection and `@Autowired` field injection are both workable styles; the
reviewable consequence is which classes are genuinely testable and whether a
required collaborator can be absent at runtime. The
[spring.threads.virtual.enabled](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.2-Release-Notes)
property (Spring Boot 3.2 or later, on Java 21) selects virtual threads for
supported runtime integration points (the release notes list Tomcat/Jetty,
request processing, the `applicationTaskExecutor` and `taskScheduler` beans,
and specific listeners); it does not convert arbitrary `ExecutorService`
fields or remove `synchronized` pinning on earlier JDKs. `ProblemDetail` is a
"representation for an RFC 9457 problem detail" with "Since: 6.0"
([javadoc](https://docs.spring.io/spring-framework/docs/6.2.19/javadoc-api/org/springframework/http/ProblemDetail.html));
a `@RestControllerAdvice` is a valid pattern, and so is route-specific
handling where one is required; neither is mandated.

## JPA persistence

`FetchType.EAGER` is "a requirement on the persistence provider runtime that
data must be eagerly fetched"
([JPA 3.1 specification](https://jakarta.ee/specifications/persistence/3.1/jakarta-persistence-spec-3.1.html));
when an entity query loads parents through a plan that does not already join
the association, the provider satisfies that requirement with separate
selects: Hibernate's user guide warns that forgetting the join fetch "will
initialize it with a secondary statement, which in turn can lead to N+1
query issues"
([Hibernate ORM 6.4 user guide](https://docs.jboss.org/hibernate/orm/6.4/userguide/html_single/Hibernate_User_Guide.html)).
Check the executed statement count for list operations rather than the
annotation names. `@ManyToOne`/`@OneToOne` default to EAGER and collections
to LAZY; a query's join plan can change what is actually issued.

`JOIN FETCH` "has the same join semantics as the corresponding inner or outer
join"; plain `JOIN FETCH` is an inner join, so parents whose collection is
empty are dropped unless the query says `LEFT JOIN FETCH`
([fetch joins, JPA 3.1 specification](https://jakarta.ee/specifications/persistence/3.1/jakarta-persistence-spec-3.1.html)).
Check each fetch-join query's result membership against callers that need
child-less rows preserved: a replacement that "fixes N+1" by dropping users
without orders is a regression for those callers. Check pagination too:
fetch joins "should usually be avoided in limited or paged queries" (same
user guide), and applying `setFirstResult`/`setMaxResults` to a
collection-fetched query is handled in memory (Hibernate 6.4 logs
"firstResult/maxResults specified with collection fetch; applying in memory"
as HHH90003004), so page composition can differ from the requested one.

Entity equality needs a deliberate definition because Hibernate proxies are
subclasses and identifier access through the conventional getter does not
initialise the proxy ("does not initialize an entity proxy when its
identifier attribute is accessed",
[Hibernate ORM 6.4 user guide](https://docs.jboss.org/hibernate/orm/6.4/userguide/html_single/Hibernate_User_Guide.html)).
In the audited Hibernate 6.4.10 the uninitialised proxy also served
identifier-based equality without initialising, while the proxy's own
`hashCode()` did initialise it: verifying such behaviour against the
project's provider and mapping is part of the review evidence. Generated
`equals`/`hashCode` covering every field (Lombok [`@Data`
generates them over all non-static, non-transient
fields](https://projectlombok.org/features/Data)) forces lazy associations
to load during comparison, which can raise `LazyInitializationException`
outside a session or give inconsistent results across proxies and detached
copies. Hibernate's user guide documents natural-key equality, or
identifier equality with a constant `hashCode` and non-transient-only
comparisons; which recipe fits depends on the mapping, inheritance, and
proxy behaviour. An entity with hand-written identifier-based equality is a
clean control; `@Data` on an `@Entity` is suspect when lazy fields are
reachable from comparison, not because a code generator was used.

## References and checklist routing

Route inspection prompts for Java through the
[common bugs checklist](common-bugs-checklist.md). The
[reference status](reference-status.md) records which claims above are
version-verified and the remaining limits. This guide does not establish
review accuracy: evaluation with fixed fixtures and agreed criteria is a
separate process.
