package invalid.example.package10.fixture;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Runs the nightly maintenance jobs and reports every outcome to the caller. */
public class BatchRunner {
    public static List<String> collectResults() throws InterruptedException {
        List<String> outcomes = new ArrayList<>();
        try (ExecutorService executor = Executors.newFixedThreadPool(2)) {
            List<Callable<String>> jobs = List.of(
                () -> "job-1-completed",
                () -> "job-2-completed",
                () -> {
                    throw new IllegalStateException("job-3 blew up");
                });
            for (Callable<String> job : jobs) {
                executor.execute(() -> {
                    try {
                        outcomes.add(job.call());
                    } catch (Exception failure) {
                        outcomes.add("job-3-failed:" + failure.getClass().getSimpleName());
                    }
                });
            }
        }
        return outcomes;
    }
}
