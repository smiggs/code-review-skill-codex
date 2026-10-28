package invalid.example.package10;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

/**
 * Shared-mutable-state contract evidence. The guide example couples the
 * read-modify-write inside the atomic compute() call, so concurrent single
 * records keep both. A check-then-act variant under the same two-record
 * submission is forced to interleave between its read and write and loses
 * exactly one record: the collection is thread-safe either way; the caller's
 * compound operation is not.
 */
class ConcurrentMapContractTest {

    interface Recordable {
        void record(String account, int amount);

        int total(String account);
    }

    /** Adapter running the exact extracted guide bytes. */
    static final class GuideLedger implements Recordable {
        private final Object ledger;
        private final Method record;
        private final Method total;

        GuideLedger() throws ReflectiveOperationException {
            Class<?> type = Extracted.type("ConcurrentLedger");
            this.ledger = type.getDeclaredConstructor().newInstance();
            this.record = type.getMethod("record", String.class, int.class);
            this.total = type.getMethod("total", String.class);
        }

        @Override
        public void record(String account, int amount) {
            try {
                record.invoke(ledger, account, amount);
            } catch (IllegalAccessException | InvocationTargetException failure) {
                throw new IllegalStateException("guide example failed to record", failure);
            }
        }

        @Override
        public int total(String account) {
            try {
                return (Integer) total.invoke(ledger, account);
            } catch (IllegalAccessException | InvocationTargetException failure) {
                throw new IllegalStateException("guide example failed to total", failure);
            }
        }
    }

    /** Defect variant: the compound read-decide-write is two separate steps. */
    static final class CheckThenActLedger implements Recordable {
        private final Map<String, Integer> totals = new ConcurrentHashMap<>();

        /** Sensitivity-only hook installed to freeze execution after the read. */
        static volatile Runnable gateAfterRead;

        @Override
        public void record(String account, int amount) {
            Integer current = totals.get(account);
            Runnable gate = gateAfterRead;
            if (gate != null) {
                gate.run();
            }
            int next = (current == null ? 0 : current) + amount;
            totals.put(account, next);
        }

        @Override
        public int total(String account) {
            return totals.getOrDefault(account, 0);
        }
    }

    @Test
    @Timeout(30)
    void guideComputeExampleKeepsBothConcurrentRecords() throws Exception {
        GuideLedger variant = new GuideLedger();
        ExecutorService pool = Executors.newFixedThreadPool(2);
        try {
            Future<?> first = pool.submit(() -> firstRecord(variant));
            Future<?> second = pool.submit(() -> firstRecord(variant));
            first.get(15, TimeUnit.SECONDS);
            second.get(15, TimeUnit.SECONDS);
        } finally {
            pool.shutdownNow();
        }
        assertEquals(2, variant.total("forced"),
            "the atomic per-key compute() kept both records under concurrent submission");
    }

    private static Void firstRecord(Recordable variant) {
        variant.record("forced", 1);
        return null;
    }

    @Test
    @Timeout(30)
    void checkThenActVariantLosesExactlyOneRecordUnderForcedInterleaving()
        throws InterruptedException, ExecutionException, TimeoutException {
        CheckThenActLedger variant = new CheckThenActLedger();
        CountDownLatch bothPastRead = new CountDownLatch(2);
        CountDownLatch proceed = new CountDownLatch(1);
        CheckThenActLedger.gateAfterRead = () -> {
            bothPastRead.countDown();
            try {
                proceed.await(5, TimeUnit.SECONDS);
            } catch (InterruptedException interrupted) {
                Thread.currentThread().interrupt();
                throw new IllegalStateException("gate thread interrupted", interrupted);
            }
        };
        ExecutorService pool = Executors.newFixedThreadPool(2);
        try {
            Future<?> first = pool.submit(() -> firstRecord(variant));
            Future<?> second = pool.submit(() -> firstRecord(variant));
            assertTrue(bothPastRead.await(5, TimeUnit.SECONDS),
                "both threads completed their read step before either write started");
            proceed.countDown();
            first.get(15, TimeUnit.SECONDS);
            second.get(15, TimeUnit.SECONDS);
        } finally {
            CheckThenActLedger.gateAfterRead = null;
            pool.shutdownNow();
        }
        assertEquals(1, variant.total("forced"),
            "the second put overwrote the first: one of two records is silently lost");
    }
}
