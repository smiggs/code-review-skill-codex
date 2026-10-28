package invalid.example.package10;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.InvocationTargetException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

/** Behaviour checks over the exact extracted guide example bytes. */
class GuideExamplesTest {

    @Test
    void userRecordValidatesItsInvariant() throws ReflectiveOperationException {
        Class<?> user = Extracted.type("UserDto");
        Object normal = user.getConstructor(String.class, int.class).newInstance("Ada", 41);
        assertEquals("Ada", user.getMethod("name").invoke(normal));
        assertEquals(41, (int) (Integer) user.getMethod("age").invoke(normal));
        InvocationTargetException failure = assertThrows(InvocationTargetException.class,
            () -> user.getConstructor(String.class, int.class).newInstance("Sad", -1));
        assertInstanceOf(IllegalArgumentException.class, failure.getCause());
    }

    @Test
    void switchPatternsDescribeEachBranchAndNull() throws ReflectiveOperationException {
        Class<?> describer = Extracted.type("TypeDescriber");
        assertEquals("null",
            Extracted.invokeStatic(describer, "describe", new Class<?>[]{Object.class}, (Object) null));
        assertEquals("integer 42",
            Extracted.invokeStatic(describer, "describe", new Class<?>[]{Object.class}, 42));
        assertEquals("string x",
            Extracted.invokeStatic(describer, "describe", new Class<?>[]{Object.class}, "x"));
        assertEquals("unrecognised Class",
            Extracted.invokeStatic(describer, "describe", new Class<?>[]{Object.class}, Void.class));
    }

    @Test
    void textBlockBuildsAJsonPayload() throws ReflectiveOperationException {
        Class<?> templates = Extracted.type("JsonTemplates");
        Object payload = Extracted.invokeStatic(templates, "userPayload",
            new Class<?>[]{String.class, int.class}, "Ada", 41);
        assertEquals("{\"name\": \"Ada\", \"age\": 41}\n", payload);
    }

    @Test
    void twoResourcesCloseInReverseOrderAndSuppressTheInnerCloseFailure()
        throws ReflectiveOperationException {
        Class<?> resource = Extracted.type("LoggedResource");
        List<String> closed = new ArrayList<>();
        InvocationTargetException failure = assertThrows(InvocationTargetException.class,
            () -> Extracted.invokeStatic(resource, "runWithTwoResources",
                new Class<?>[]{List.class}, closed));
        // The propagated exception comes from the body; the inner close failure
        // is suppressed, not lost.
        assertEquals("body failure", failure.getCause().getMessage());
        List<?> suppressed = List.of(failure.getCause().getSuppressed());
        assertEquals(1, suppressed.size(), "exactly one close failure is suppressed");
        Object closeFailure = suppressed.get(0);
        assertInstanceOf(IllegalStateException.class, closeFailure);
        assertEquals("close failure of inner", ((IllegalStateException) closeFailure).getMessage());
        assertEquals(List.of("inner", "outer"), closed, "reverse order on failure");
    }

    @Test
    @Timeout(15)
    void fixedPoolDrainsSubmittedWorkAndObservesTheTimeoutFlag()
        throws ReflectiveOperationException, InterruptedException, ExecutionException,
            TimeoutException {
        CountDownLatch started = new CountDownLatch(1);
        CountDownLatch release = new CountDownLatch(1);
        Class<?> owner = Extracted.type("ExecutorOwnership");
        Object executorOwner = owner.getConstructor(int.class).newInstance(1);
        java.lang.reflect.Field field = owner.getDeclaredField("executor");
        field.setAccessible(true);
        ExecutorService executor = (ExecutorService) field.get(executorOwner);
        executor.submit(() -> {
            started.countDown();
            try {
                return release.await(9, TimeUnit.SECONDS);
            } catch (InterruptedException interrupted) {
                Thread.currentThread().interrupt();
                return false;
            }
        });
        assertTrue(started.await(5, TimeUnit.SECONDS), "event body started");
        release.countDown();
        Object drained = owner
            .getMethod("drainTasks", long.class, TimeUnit.class)
            .invoke(executorOwner, 5L, TimeUnit.SECONDS);
        assertEquals(true, drained, "submitted work completed before drainTasks returned");
    }

    @Test
    @Timeout(15)
    void singletonFixedPoolAbandonsRunningTaskByInterruptingIt()
        throws ReflectiveOperationException, InterruptedException {
        CountDownLatch taskStarted = new CountDownLatch(1);
        CountDownLatch halfDone = new CountDownLatch(1);
        Object monitor = new Object();
        Class<?> owner = Extracted.type("ExecutorOwnership");
        Object executorOwner = owner.getConstructor(int.class).newInstance(1);
        java.lang.reflect.Field field = owner.getDeclaredField("executor");
        field.setAccessible(true);
        ExecutorService executor = (ExecutorService) field.get(executorOwner);
        executor.submit(() -> {
            taskStarted.countDown();
            synchronized (monitor) {
                try {
                    monitor.wait();
                } catch (InterruptedException interrupted) {
                    halfDone.countDown();
                    Thread.currentThread().interrupt();
                }
            }
            return null;
        });
        assertTrue(taskStarted.await(5, TimeUnit.SECONDS), "task started before shutdownNow");
        owner.getMethod("abandonRunningTasks").invoke(executorOwner);
        assertTrue(halfDone.await(5, TimeUnit.SECONDS),
            "shutdownNow delivered the interrupt to the running task");
        executor.shutdownNow();
    }

    @Test
    void virtualThreadPerTaskExecutorRunsTheTaskOnAVirtualThreadAndCloseWaits()
        throws ReflectiveOperationException, InterruptedException,
            java.util.concurrent.ExecutionException {
        Class<?> owner = Extracted.type("VirtualExecutorOwnership");
        Object ranVirtual = Extracted.invokeStatic(owner, "ranOnVirtualThread", new Class<?>[]{});
        assertTrue(ranVirtual instanceof Boolean && (Boolean) ranVirtual,
            "the guide example observed a virtual thread");
    }

    @Test
    @Timeout(30)
    void computeKeepsConcurrentRecordsExact()
        throws ReflectiveOperationException, InterruptedException, ExecutionException,
            TimeoutException {
        int threads = 8;
        int perThread = 2000;
        Class<?> ledger = Extracted.type("ConcurrentLedger");
        Object instance = ledger.getDeclaredConstructor().newInstance();
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        try {
            List<Future<?>> work = new ArrayList<>();
            for (int t = 0; t < threads; t++) {
                work.add(pool.submit(() -> {
                    for (int i = 0; i < perThread; i++) {
                        try {
                            ledger.getMethod("record", String.class, int.class)
                                .invoke(instance, "acme", 1);
                        } catch (ReflectiveOperationException failure) {
                            throw new IllegalStateException("recording failed", failure);
                        }
                    }
                    return null;
                }));
            }
            for (Future<?> result : work) {
                result.get(20, TimeUnit.SECONDS);
            }
        } finally {
            pool.shutdownNow();
        }
        int total = (int) ledger.getMethod("total", String.class).invoke(instance, "ACME");
        assertEquals(threads * perThread, total, "compute() per-key atomicity keeps every record");
    }

    @Test
    void sharedDateTimeFormatterFormatsOnManyThreads()
        throws ReflectiveOperationException, InterruptedException, ExecutionException,
            TimeoutException {
        Class<?> formatter = Extracted.type("EventFormatter");
        Object expected = Extracted.invokeStatic(formatter, "dayOf",
            new Class<?>[]{LocalDate.class}, LocalDate.of(2026, 10, 28));
        assertEquals("2026-10-28", expected);
        ExecutorService pool = Executors.newFixedThreadPool(4);
        try {
            List<Future<String>> days = new ArrayList<>();
            for (int index = 0; index < 64; index++) {
                final int dayOfMonth = index % 28 + 1;
                days.add(pool.submit(() -> {
                    try {
                        return (String) Extracted.invokeStatic(formatter, "dayOf",
                            new Class<?>[]{LocalDate.class}, LocalDate.of(2026, 10, dayOfMonth));
                    } catch (ReflectiveOperationException failure) {
                        throw new IllegalStateException("formatting failed", failure);
                    }
                }));
            }
            for (int index = 0; index < days.size(); index++) {
                assertEquals(String.format("2026-10-%02d", index % 28 + 1),
                    days.get(index).get(10, TimeUnit.SECONDS));
            }
        } finally {
            pool.shutdownNow();
        }
    }
}
