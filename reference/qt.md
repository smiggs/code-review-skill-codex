# Qt review guide

Use this guide under the [review contract](review-contract.md). Ground
findings in reachable lifetime, threading, or event-loop failures and in the
project's Qt version. Naming conventions, layout preferences, and string
helpers alone are not defects.

## Versions and review scope

Read the build configuration for the Qt major and minor version
(`find_package(Qt6 ...)` or a `.pro` file), the modules linked, and whether
the target is widgets, QML, or a non-GUI process. The documentation checks
below were made against the Qt 6.12 online documentation accessed on
29 October 2026; Qt 5.15 differences are marked where they change the
advice. Qt 6 code is source-compatible across minor releases, but
connection-type and literal availability have version boundaries, so check
the project's own version first. See the
[reference status](reference-status.md) for verification limits.

## Parent ownership and object lifetime

A QObject's parent takes ownership: the parent's destructor destroys all
child objects, and a child created with a parent must not also be deleted by
hand. A child that lives on the stack or as a global while it has a heap
parent is destroyed twice if the parent is destroyed first, which the
[QObject documentation](https://doc.qt.io/qt-6/qobject.html) warns leads to
a crash; a child destroyed first removes itself from the parent. An unparented heap object needs another stated owner, such as a
`std::unique_ptr`, or a documented transfer into the object tree.

```cpp
auto* label = new QLabel(parentWidget); // parentWidget owns label.
```

Ownership and thread affinity are linked: all QObjects must live in the same
thread as their parent, `setParent()` fails across threads, and
`moveToThread()` fails for an object that has a parent. A QObject lives in
the thread that created it; queued signals and posted events are delivered
in that thread. Creating QObjects before the `QApplication` (or
`QCoreApplication`) exists is unsupported and can crash at exit.

`QPointer` gives a guarded pointer that the QObject destructor clears to
null; it is for references to objects owned elsewhere, not an ownership
mechanism. Mixing `std::shared_ptr` with parent ownership can destroy an
object twice, because the parent and the shared owner both release it, so a
QObject managed by a parent must not also be owned by a shared pointer.
`QScopedPointer` (Qt 5 idiom) and `std::unique_ptr` both work for unparented
objects; prefer the project's existing convention.

## Deferred deletion

`deleteLater()` schedules deletion for when control returns to the event
loop. The documented contract has edges worth checking: the deletion happens
when the loop that called it regains control (a nested modal loop does not
trigger it); if the object's thread has no running event loop, the object is
destroyed when the thread finishes; if it is called after the main event
loop has stopped, the object is not deleted at all. The call is thread-safe.
Deleting a QObject directly from a slot that the same object's signal
invoked destroys the emitter mid-delivery; `deleteLater()` avoids that and
is documented as often safer in `~QObject`-related cleanup. Where a plain
`delete` is reachable inside a slot, an event handler, or a lambda
connected to the object's own signals, check whether deferred deletion is
the correct contract.

## Signals, slots, and connections

Function-pointer connections are checked at compile time; the string-based
`SIGNAL()`/`SLOT()` macros are checked only at runtime, so a typo compiles
and silently connects nothing. That runtime-only failure is the trigger, and
it matters most where the connected pair is exercised rarely.

The connection type decides which thread runs the slot and when. The
documented semantics:

| Type | Effect |
| --- | --- |
| `Qt::AutoConnection` (default) | Decided when the signal is emitted: direct if the receiver lives in the emitting thread, otherwise queued. |
| `Qt::DirectConnection` | The slot runs immediately in the emitting thread. |
| `Qt::QueuedConnection` | The slot runs when the receiver's thread event loop regains control; arguments are copied, so custom types must be registered with `qRegisterMetaType`. |
| `Qt::BlockingQueuedConnection` | Like queued, but the emitting thread blocks. It deadlocks if the receiver lives in the emitting thread. |
| `Qt::UniqueConnection` | Flag combined with the types above; `connect` fails if the connection already exists. Uniqueness is not enforced for lambdas, functors, or non-member functions, so duplicate invocations remain possible there. |

A direct connection across threads runs slot code in the wrong thread; with
queued connections, an unregistered argument type fails to deliver at
runtime. Review the thread that each side lives in, not the connection site
alone.

The contextless overload, `connect(sender, &Sender::sig, lambda)`, is
disconnected when the sender is destroyed but does not track any captured
owner, so a captured raw pointer can outlive its owner and be used after
destruction. Passing a context object

```cpp
connect(sender, &Sender::valueChanged, worker, [this](int v) {
    update(v);
});
```

disconnects the lambda when `worker` (here `this`'s peer) is destroyed and
makes the invocation follow the context object's thread affinity. Capturing
`this` or widget pointers without a context object is a dangling-capture
trigger whenever the emitting sender can outlive the captured owner.

Guarding a setter against re-entrant signal loops with an equality check is
a valid control, not a defect:

```cpp
void MyClass::setValue(int v) {
    if (m_value == v) {
        return;
    }
    m_value = v;
    emit valueChanged(v);
}
```

## Threads and the worker-object pattern

The worker-object pattern moves a QObject into a thread and drives it by
signals; the [QThread documentation](https://doc.qt.io/qt-6/qthread.html)
recommends connecting `finished()` to `deleteLater()` to free the worker.
The lifecycle below is the shape to check for: the thread stops through
`quit()`, the worker and thread delete themselves after `finished()`, and
the owner waits for completion before destroying anything itself.

```cpp
auto* thread = new QThread;
auto* worker = new Worker;
worker->moveToThread(thread);
connect(thread, &QThread::started, worker, &Worker::process);
connect(worker, &Worker::finished, thread, &QThread::quit);
connect(thread, &QThread::finished, worker, &QObject::deleteLater);
connect(thread, &QThread::finished, thread, &QObject::deleteLater);
thread->start();
```

Subclassing `QThread` and reimplementing `run()` is a documented, valid
approach; do not report it as a defect by itself. The conditions that make
it fail are specific: the `QThread` object itself lives in the creating
thread, so slots declared on the subclass execute in the wrong thread; the
documentation states new slots should not be implemented directly in a
subclassed `QThread`. `run()` without `exec()` has no event loop, so
`deleteLater()` and queued calls cannot be delivered inside it. Deleting a
running `QThread` crashes; wait for `finished()` (or call `wait()`) first.
`QThread` member functions such as `setPriority()` may only be called from
the creating thread unless documented otherwise.

Widget classes are main-thread-only: the GUI classes, notably `QWidget` and
all its subclasses, are not reentrant and can only be used from the main
thread. Accessing a widget from a worker thread is a defect trigger; the fix
is a queued signal to the main thread. The same single-thread model applies
to each non-GUI QObject: creating an object in one thread and calling its
functions from another is not guaranteed to work.

Long operations on the main thread freeze the event loop, which blocks
painting and input. Moving work to a worker thread, `QtConcurrent`,
`QProcess`, or an asynchronous API is the check; a synchronous network or
file call on the GUI thread is the trigger. Whether the delay is user-visible
depends on the workload, so state the consequence.

## Strings and containers

`QStringLiteral` and the Qt 6.4 literals `u"..."_s` and `u"..."_L1` (in the
`Qt::Literals::StringLiterals` namespace) avoid runtime conversion and
allocation that a plain `const char*` comparison performs; Qt 5 uses
`QStringLiteral` and `QLatin1String` instead. Comparing or assigning a
`QString` from `const char*` converts UTF-8 data at runtime and can
allocate; defining `QT_NO_CAST_FROM_ASCII` disables the implicit conversion
and turns the encoding risk into a compile error. These are efficiency and
encoding prompts: check the project's own string conventions before
reporting.

Qt 6 `QList` is a contiguous array and `QVector` is an alias to it. In Qt 5
the two differ, and the Qt documentation recommended `QVector` for
predictable performance with large types. A container passed by value is
implicitly shared: the copy is cheap until a non-const operation detaches,
and `at()` never detaches. Passing by `const&` for read-only parameters is
the conventional shape; a by-value parameter is a defect trigger only when
the callee mutates the container and forces a deep copy on a hot path.

## Meta-object system

`qobject_cast<T*>` works on QObject-derived types that declare `Q_OBJECT`;
it returns null for an unrelated type instead of throwing, and unlike
`dynamic_cast` it needs no RTTI. A cast of a class that forgot `Q_OBJECT`
compiles with the base meta-object and returns null at runtime, so a null
result is the symptom to trace. `Q_PROPERTY` exposes values to
introspection and QML; `Q_ENUM` registers an enum with the meta-object
system. Their absence is a defect only where the property or enum must be
visible to that machinery.

## References and checklist routing

Route inspection prompts for Qt through the
[common bugs checklist](common-bugs-checklist.md). The
[reference status](reference-status.md) records which claims above are
version-verified and the remaining limits. This guide does not establish
review accuracy: evaluation with fixed fixtures and agreed criteria is a
separate process.
