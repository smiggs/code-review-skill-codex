// Class declaration for the guarded-setter fence. The extracted fence
// defines MyClass::setValue out of line; Q_OBJECT support comes from moc.
#pragma once
#include <QObject>

class MyClass : public QObject {
    Q_OBJECT
    int m_value = -1;
public:
    using QObject::QObject;
    void setValue(int v); // Defined by the extracted fence.
    int value() const { return m_value; }
signals:
    void valueChanged(int v);
};
