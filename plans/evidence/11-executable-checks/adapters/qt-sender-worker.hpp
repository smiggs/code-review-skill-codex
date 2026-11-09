// Shared Qt classes for the guide harness. Q_OBJECT classes need moc.
#pragma once
#include <QObject>
#include <QThread>

class Sender : public QObject {
    Q_OBJECT
public:
    using QObject::QObject;
    void emitChanged(int v) { emit valueChanged(v); }
signals:
    void valueChanged(int v);
};

class Worker : public QObject {
    Q_OBJECT
public:
    using QObject::QObject;
    void process() { emit finished(); }
signals:
    void finished();
};
