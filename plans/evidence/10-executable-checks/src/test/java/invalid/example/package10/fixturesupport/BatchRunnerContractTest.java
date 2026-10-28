package invalid.example.package10.fixturesupport;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.api.condition.EnabledIfSystemProperty;

/**
 * Contract test for the failure-observability fixture. The harness copies
 * either the clean base or the defective head into
 * invalid.example.package10.fixture before running. These tests are enabled only when the harness passes -Dpackage10fixture=true.
 */
class BatchRunnerContractTest {

    @Test
    @Timeout(60)
    @EnabledIfSystemProperty(named = "package10fixture", matches = "true")
    void nightlyRunKeepsEveryJobOutcomeObservable() throws Exception {
        List<?> outcomes = (List<?>) Class.forName("invalid.example.package10.fixture.BatchRunner")
            .getMethod("collectResults")
            .invoke(null);
        assertTrue(outcomes.size() == 3,
            "all three nightly jobs must publish an outcome; observed: " + outcomes);
        assertTrue(outcomes.stream().anyMatch(element -> stringOf(element).startsWith("job-3-failed")),
            "every task failure must stay observable to the caller; observed: " + outcomes);
        assertTrue(outcomes.stream().anyMatch(element -> stringOf(element).equals("job-1-completed")),
            "successful jobs remain observed");
        assertTrue(outcomes.stream().anyMatch(element -> stringOf(element).equals("job-2-completed")),
            "successful jobs remain observed");
    }

    private static String stringOf(Object value) {
        return String.valueOf(value);
    }
}
