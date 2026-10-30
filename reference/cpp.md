# C++ review guide

Use this guide under the [review contract](review-contract.md). Ground
findings in reachable lifetime failures, ownership contracts, or project
requirements. Smart-pointer choice, allocation patterns, and template style
alone are not defects.

## Versions and review scope

Read the build configuration for the compiler, the `-std=` flag
(`c++17`, `c++20`, or later), warning and sanitiser options, and any
library or framework versions that own lifetime rules. The executable audit
baseline is GCC 13.3.0 on Linux/x86_64 for C++17 and C++20; retained examples
were compiled and exercised there. `std::span` and constrained templates
require C++20; `std::expected` is C++23 and is unavailable in a C++17/20
build. See the [reference status](reference-status.md) for verification
limits.

## Ownership and RAII

Prefer types that own their resources: `std::unique_ptr` by default,
`std::shared_ptr` only where the lifetime is genuinely shared and the
ownership is documented. A raw `new`/`delete` pair is a review prompt, not a
defect by itself; the trigger is an ownership transfer or an error path the
code does not handle.

```cpp
std::unique_ptr<Foo> make_foo() {
    auto foo = std::make_unique<Foo>();
    if (!foo->Init()) {
        return {};
    }
    return foo;
}
```

C resources need an owner with a stated deleter. A `std::unique_ptr` with a
function-pointer deleter such as `fclose` does not invoke the deleter for a
null pointer, so a failed `fopen` is safe; the type still needs a documented
contract for whether a null `FILE*` is a valid state.

```cpp
using FilePtr = std::unique_ptr<FILE, decltype(&fclose)>;

FilePtr open_file(const char* path) {
    return FilePtr(fopen(path, "rb"), &fclose);
}
```

## Lifetime and views

`std::string_view` and `std::span` do not own the characters or elements
they refer to; it is the programmer's responsibility to keep the owner alive
for the view's lifetime (see the
[`std::string_view` ownership note](https://en.cppreference.com/w/cpp/string/basic_string_view.html)).
A view of a temporary or of a function-local string dangles at return. The
trigger is the view escaping the scope of its owner: a returned view, a
stored view, or a view captured by a lambda that outlives the owner.

```cpp
std::string_view good_view(const std::string& s) {
    return s; // Caller owns the storage for the duration of the call.
}

std::string good_name() {
    return make_name(); // Return an owner when the value must escape.
}
```

Reference captures in lambdas dangle the same way: a lambda stored or
invoked after the captured object's scope ends must capture by value or
hold a documented owner.

```cpp
std::function<void()> make_task() {
    int value = 42;
    return [value]() { use(value); };
}
```

## Copy and move correctness

Prefer the rule of zero: members that manage themselves (`std::vector`,
`std::string`, smart pointers) remove the need for user-defined special
members.

```cpp
struct Buffer {
    std::vector<int> data;
    explicit Buffer(size_t n) : data(n) {}
};
```

When a class owns a raw resource and declares a destructor, the copy
constructor and copy assignment are still implicitly generated (deprecated
since C++11) and copy the owning pointer, so two objects destroy the same
resource; the move operations are not generated at all
([implicit copy is deprecated](https://eel.is/c++draft/depr.impldec),
[moves require no user-declared special members](https://eel.is/c++draft/class.copy.ctor)).
Define or delete the missing operations explicitly.

A defaulted move operation is memberwise copy. For a class whose destructor
releases a raw handle, defaulted moves leave the source owning the same
handle as the destination, and both destructors release it, which is a double close
or double free reachable through any move of the object. The move must
transfer the handle and reset the source, or the class must delete its moves
if it has no need for them.

```cpp
class Socket {
public:
    Socket() = default;
    explicit Socket(int fd) : fd_(fd) {}
    ~Socket() {
        if (fd_ != kInvalid) {
            close(fd_);
        }
    }

    Socket(const Socket&) = delete;
    Socket& operator=(const Socket&) = delete;

    Socket(Socket&& other) noexcept : fd_(std::exchange(other.fd_, kInvalid)) {}
    Socket& operator=(Socket&& other) noexcept {
        if (this != &other) {
            if (fd_ != kInvalid) {
                close(fd_);
            }
            fd_ = std::exchange(other.fd_, kInvalid);
        }
        return *this;
    }

private:
    static constexpr int kInvalid = -1;
    int fd_ = kInvalid;
};
```

After this contract, a moved-from `Socket` owns nothing and closes nothing;
the destination closes the handle exactly once. Deleting both move
operations instead is equally valid where moves are not required. A class
with defaulted moves is correct only when its members manage themselves, as
in the rule-of-zero `Buffer` above.

## API design and inheritance

`const`-correct accessors, `explicit` converting constructors, passing
polymorphic types by reference to avoid slicing, and `override`/`final` on
virtual functions make contracts checkable. Missing `override` on a
would-be overriding function is a trigger only when the signatures actually
diverge or the base function changes; check the declarations before
reporting. Slicing is a defect trigger when a derived object is copied into
a base by value and behaviour depends on the derived part.

## Exception safety and error results

RAII types clean up during unwinding; a destructor must not let an exception
escape, and destructors are implicitly `noexcept`. Distinguish normal,
expected failures (return `std::optional`, a status type, or C++23's
`std::expected` where the project has adopted it) from invariant failures
that justify an exception. `std::stoi` throws `std::invalid_argument` and
`std::out_of_range`; a wrapper that converts those to a result type states
its contract:

```cpp
std::optional<int> parse_int(const std::string& s) {
    try {
        return std::stoi(s);
    } catch (const std::exception&) {
        return std::nullopt;
    }
}
```

## Concurrency

Concurrent unsynchronised access to shared data, with at least one write, is
a data race and undefined behaviour.

```cpp
std::atomic<int> counter{0};
void inc() { counter.fetch_add(1, std::memory_order_relaxed); }
```

`relaxed` ordering needs a stated invariant (here: a count with no ordering
requirements); `std::mutex` with an RAII lock guard covers multi-step
invariants on shared state:

```cpp
std::mutex mu;
std::vector<int> data;

void add(int v) {
    std::lock_guard<std::mutex> lock(mu);
    data.push_back(v);
}
```

Holding a lock across blocking operations, inconsistent lock ordering, and
check-then-act sequences split across lock acquisitions are the concrete
triggers; report them where callers can reach the failure.

## Performance patterns as advice

`reserve`, move semantics, and string building change allocation behaviour,
not correctness. `std::vector::reserve` throws `std::length_error` when the
requested capacity exceeds `max_size()`
([vector.capacity](https://eel.is/c++draft/vector.capacity)), so converting
a signed count to `size_t` without validation silently turns a negative
input into a huge request. Validate the input contract first:

```cpp
std::vector<int> build(int n) {
    if (n < 0) {
        throw std::invalid_argument("count must be non-negative");
    }
    std::vector<int> out;
    out.reserve(static_cast<size_t>(n));
    for (int i = 0; i < n; ++i) {
        out.push_back(i);
    }
    return out;
}
```

Report allocation patterns only with evidence of the workload impact, such
as a profile or a documented performance requirement; a loop without
`reserve` alone is not a defect.

## Templates and type safety

Constrained templates (`requires`) are C++20; in a C++17 build the same
intent needs `static_assert` or SFINAE. `static_assert` on
`std::is_trivially_copyable_v` documents a real invariant for types stored
or transmitted as raw bytes. Report unconstrained templates only when an
instantiation produces a wrong or surprising result, not as style.

## Tooling and build checks

Warnings, sanitiser builds, and static analysis are review evidence, not
verdicts. A clean run does not prove the absence of undefined behaviour.

```bash
# Warnings and language mode (read-only checks)
g++ -std=c++20 -Wall -Wextra -Wconversion -Wshadow -c src.cpp

# Sanitisers (debug builds)
g++ -std=c++20 -fsanitize=address,undefined -fno-omit-frame-pointer -g -c src.cpp
g++ -std=c++20 -fsanitize=thread -fno-omit-frame-pointer -g -c src.cpp

# Static analysis (read-only)
clang-tidy src.cpp -- -std=c++20
```

Formatting rewrites the working tree; propose it as a separate authorised
edit, not as a review check.

## References and checklist routing

Route inspection prompts for C++ through the
[common bugs checklist](common-bugs-checklist.md). The
[reference status](reference-status.md) records which claims above are
version-verified and the remaining limits. This guide does not establish
review accuracy: evaluation with fixed fixtures and agreed criteria is a
separate process.
