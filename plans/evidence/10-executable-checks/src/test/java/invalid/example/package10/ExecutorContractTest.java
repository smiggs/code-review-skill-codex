package invalid.example.package10;


import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

/**
 * JDK 21 executor contracts exercised directly: Future.cancel(true)
 * interrupts a started task, and AutoCloseable close() waits for submitted
 * work (documented addition from JDK 19, final in JDK 21).
 */
class ExecutorContractTest {

    @Test
    @Timeout(15)
    void futureCancelDeliversTheInterruptToAStartedTask()
        throws InterruptedException, java.util.concurrent.ExecutionException {
        CountDownLatch taskStarted = new CountDownLatch(1);
        CountDownLatch interruptSeen = new CountDownLatch(1);
        ExecutorService pool = Executors.newFixedThreadPool(1);
        try {
            Future<?> handle = pool.submit(() -> {
                taskStarted.countDown();
                try {
                    TimeUnit.SECONDS.sleep(9);
                } catch (InterruptedException interrupted) {
                    interruptSeen.countDown();
                    Thread.currentThread().interrupt();
                    return null;
                }
                return null;
            });
            assertTrue(taskStarted.await(5, TimeUnit.SECONDS), "task started");
            boolean cancelled = handle.cancel(true);
            assertTrue(cancelled, "a started task is cancelled when interruption is requested");
            assertTrue(interruptSeen.await(5, TimeUnit.SECONDS),
                "cancel(true) reached the running task as an interrupt");
        } finally {
            pool.shutdownNow();
        }
        assertTrue(pool.awaitTermination(2, TimeUnit.SECONDS),
            "the pool terminates promptly after shutdownNow");
    }

    @Test
    @Timeout(15)
    void tryWithResourceCloseWaitsForTheSubmittedTaskToFinish() throws InterruptedException {
        CountDownLatch taskStarted = new CountDownLatch(1);
        CountDownLatch release = new CountDownLatch(1);
        AtomicBoolean finishedOnTime = new AtomicBoolean(false);
        Thread releaser = new Thread(() -> {
            try {
                TimeUnit.MILLISECONDS.sleep(250);
                release.countDown();
            } catch (InterruptedException interrupted) {
                Thread.currentThread().interrupt();
            }
        });
        releaser.setDaemon(true);
        releaser.start();
        try (ExecutorService executor = Executors.newFixedThreadPool(1)) {
            executor.submit(() -> {
                taskStarted.countDown();
                try {
                    release.await(9, TimeUnit.SECONDS);
                    finishedOnTime.set(true);
                } catch (InterruptedException interrupted) {
                    Thread.currentThread().interrupt();
                }
                return null;
            });
            assertTrue(taskStarted.await(5, TimeUnit.SECONDS), "task started before close() ran");
        }
        assertTrue(finishedOnTime.get(),
            "close() ran only after the submitted task completed its work");
    }
}
