#include "classes.hpp"
#include <QCoreApplication>
#include <QPointer>
#include <cstdio>

/* The lambda keeps no context object: the connection survives the owner. */
int qt_lambda_calls = 0;

int main(int argc, char** argv) {
    QCoreApplication app(argc, argv);
    Sender sender;
    QPointer<Owner> owner;
    {
        auto* owned = new Owner;
        owner = owned;
        QObject::connect(&sender, &Sender::valueChanged, [owned](int) {
            ++qt_lambda_calls;
            (void)owned;
        });
        sender.poke(1);
        QCoreApplication::processEvents();
        delete owned;
    }
    sender.poke(2);
    QCoreApplication::processEvents();
    std::printf("ownerAlive=%d calls=%d\n",
                static_cast<int>(!owner.isNull()), qt_lambda_calls);
    return 0;
}
