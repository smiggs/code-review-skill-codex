// Verifies the qobject_cast and QPointer claims made in the guide prose.
#include "qt-sender-worker.hpp"
#include <QCoreApplication>
#include <QPointer>
#include <cstdio>

static int failures = 0;
static void check(bool ok, const char* what) {
    printf("%-46s %s\n", what, ok ? "ok" : "FAIL");
    if (!ok) {
        failures++;
    }
}

int main(int argc, char** argv) {
    QCoreApplication app(argc, argv);
    Sender sender;
    QObject plain;
    check(qobject_cast<Sender*>(&sender) == &sender, "qobject_cast returns the object");
    check(qobject_cast<Worker*>(&sender) == nullptr,
          "qobject_cast returns null for an unrelated type");
    check(qobject_cast<Sender*>(&plain) == nullptr,
          "qobject_cast returns null for a plain QObject");

    QPointer<Sender> guard = &sender;
    check(!guard.isNull(), "QPointer tracks a live object");
    {
        Sender temporary;
        QPointer<Sender> dying = &temporary;
        check(!dying.isNull(), "QPointer tracks before destruction");
    }
    QPointer<Sender> after;
    {
        Sender temporary;
        after = &temporary;
    }
    check(after.isNull(), "QPointer clears after destruction");
    printf("%s\n", failures ? "FAILURES" : "ALL-OK");
    return failures ? 1 : 0;
}
