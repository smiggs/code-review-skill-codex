// Shared Q_OBJECT classes for the context-lambda fixture pair.
#pragma once
#include <QObject>
#include <QPointer>

class Owner : public QObject {
    Q_OBJECT
public:
    using QObject::QObject;
};

class Sender : public QObject {
    Q_OBJECT
public:
    using QObject::QObject;
    void poke(int v) { emit valueChanged(v); }
signals:
    void valueChanged(int v);
};
