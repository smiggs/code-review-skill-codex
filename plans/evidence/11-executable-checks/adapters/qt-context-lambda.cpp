// Verifies the context-object lambda contract: the connection is
// disconnected when the context object dies. ContextHost holds the lambda's
// captures and needs no Q_OBJECT of its own.
#include "qt-sender-worker.hpp"
#include <QCoreApplication>
#include <QPointer>
#include <cstdio>

int qt_context_calls = 0;

class ContextHost : public QObject {
public:
    using QObject::QObject;
    void arm(Sender* sender, Worker* worker); // Defined by the extracted fence.
    void update(int v);
};

void ContextHost::arm(Sender* sender, Worker* worker) {
    /* FENCE:1 */
}

void ContextHost::update(int v) {
    ++qt_context_calls;
    (void)v;
}

static int failures = 0;
static void check(bool ok, const char* what) {
    printf("%-46s %s\n", what, ok ? "ok" : "FAIL");
    if (!ok) {
        failures++;
    }
}

int main(int argc, char** argv) {
    QCoreApplication app(argc, argv);
    {
        auto* sender = new Sender;
        auto* worker = new Worker;
        auto* host = new ContextHost;
        host->arm(sender, worker);
        sender->emitChanged(1);
        QCoreApplication::processEvents();
        check(qt_context_calls == 1, "context connection delivers directly");
        delete worker; // The fence passes worker as the context object.
        sender->emitChanged(2);
        QCoreApplication::processEvents();
        check(qt_context_calls == 1,
              "destroyed context auto-disconnects the lambda");
        delete host;
        delete sender;
    }
    printf("%s\n", failures ? "FAILURES" : "ALL-OK");
    return failures ? 1 : 0;
}
