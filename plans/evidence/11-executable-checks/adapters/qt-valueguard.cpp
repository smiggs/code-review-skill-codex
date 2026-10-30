// Verifies the guarded setter fence: duplicate values emit nothing.
#include "qt-valueguard-classes.hpp"
#include <QCoreApplication>
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
    MyClass object;
    int changes = 0;
    QObject::connect(&object, &MyClass::valueChanged,
                     [&changes](int) { ++changes; });
    object.setValue(1);
    object.setValue(1);
    object.setValue(2);
    check(object.value() == 2, "guarded setter stores the new value");
    check(changes == 2, "guarded setter skips duplicate emissions");
    printf("%s\n", failures ? "FAILURES" : "ALL-OK");
    return failures ? 1 : 0;
}

// The extracted fence defines MyClass::setValue out of line.
/* FENCE:2 */
