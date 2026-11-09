// Verifies the worker-object lifecycle from the guide fence: started work
// runs in the thread, quit stops it, and finished deletes worker and thread.
#include "qt-sender-worker.hpp"
#include <QCoreApplication>
#include <QElapsedTimer>
#include <QPointer>
#include <cstdio>
#include <functional>

static int failures = 0;
static void check(bool ok, const char* what) {
    printf("%-46s %s\n", what, ok ? "ok" : "FAIL");
    if (!ok) {
        failures++;
    }
}

static bool wait_until(const std::function<bool()>& predicate, int ms) {
    QElapsedTimer timer;
    timer.start();
    while (!predicate()) {
        if (timer.elapsed() > ms) {
            return false;
        }
        QCoreApplication::processEvents();
        QThread::msleep(10);
    }
    return true;
}

int main(int argc, char** argv) {
    QCoreApplication app(argc, argv);

    // The guide shows the fence in a class context, where unqualified
    // connect resolves to QObject::connect; this free function selects the
    // same static overload by macro without touching the extracted bytes.
#define connect QObject::connect

    // The extracted fence creates, connects, and starts both objects; the
    // locals below continue in the fence's scope.
    /* FENCE:3 */
    QPointer<Worker> workerGuard = worker;
    QPointer<QThread> threadGuard = thread;

    check(!workerGuard.isNull(), "worker object exists after start");
    check(wait_until([&]() { return !thread->isRunning(); }, 10000),
          "thread stops through the quit connection");
    check(wait_until([&]() { return workerGuard.isNull(); }, 10000),
          "finished deletes the worker");
    check(wait_until([&]() { return threadGuard.isNull(); }, 10000),
          "finished deletes the thread");

    printf("%s\n", failures ? "FAILURES" : "ALL-OK");
    return failures ? 1 : 0;
}
