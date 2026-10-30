// Verifies the parent-ownership fence for widgets. Requires a Qt Widgets
// build with a usable platform plugin (offscreen); the runner skips this
// adapter and records the limit when neither is available.
#include <QApplication>
#include <QLabel>
#include <QPointer>
#include <QWidget>
#include <cstdio>

static int failures = 0;
static void check(bool ok, const char* what) {
    printf("%-46s %s\n", what, ok ? "ok" : "FAIL");
    if (!ok) {
        failures++;
    }
}

static QWidget* make_child(QWidget* parentWidget) {
    /* FENCE:0 */
    return label;
}

int main(int argc, char** argv) {
    QApplication app(argc, argv);
    auto* parent = new QWidget;
    QPointer<QWidget> child = make_child(parent);
    check(!child.isNull(), "child exists with its parent");
    check(child->parent() == parent, "constructor records the parent owner");
    delete parent;
    check(child.isNull(), "parent destruction deletes the child");
    printf("%s\n", failures ? "FAILURES" : "ALL-OK");
    return failures ? 1 : 0;
}
