// Test driver for the C++ guide units. This file is concatenated AFTER the
// extracted reference/cpp.md fences into one translation unit, so the unit
// definitions above are visible here directly.
#include "cpp-prelude.hpp"

#include <exception>
#include <type_traits>

static int failures = 0;

static void check(bool ok, const std::string& what) {
    printf("%-46s %s\n", what.c_str(), ok ? "ok" : "FAIL");
    if (!ok) {
        failures++;
    }
}

static void test_make_foo(void) {
    foo_init_succeeds = true;
    auto ok = make_foo();
    check(static_cast<bool>(ok) && ok->Init(), "make_foo returns an owner");
    foo_init_succeeds = false;
    auto bad = make_foo();
    check(!bad, "make_foo returns empty on failed Init");
    foo_init_succeeds = true;
}

static void test_open_file(void) {
    FilePtr f = open_file("/dev/null");
    check(f.get() != nullptr, "open_file opens an existing file");
    f.reset();
    FilePtr missing = open_file("/definitely-missing-codex.file");
    check(missing.get() == nullptr, "open_file tolerates a missing path");
}

static void test_views(void) {
    std::string owner = "hello world";
    std::string_view view = good_view(owner);
    check(view.size() == 11 && view[0] == 'h', "good_view reads caller-owned data");
    check(good_name() == make_name_value, "good_name returns an owned copy");
}

static void test_make_task(void) {
    auto task = make_task();
    check(task != nullptr, "make_task returns a callable");
    task();
    task();
}

static void test_buffer(void) {
    Buffer b(5);
    b.data[0] = 1;
    Buffer copy = b;
    copy.data[0] = 2;
    check(b.data[0] == 1 && copy.data[0] == 2,
          "Buffer copies own independent storage");
}

static void test_socket_moves(void) {
    check(!std::is_copy_constructible<Socket>::value,
          "Socket rejects copies");
    socket_close_calls = 0;
    {
        Socket owner(5);
        {
            Socket moved = std::move(owner);
            check(socket_close_calls == 0, "moving does not close");
        }
        check(socket_close_calls == 1, "destruction closes exactly once");
    }
    check(socket_close_calls == 1, "moved-from Socket closes nothing");

    socket_close_calls = 0;
    {
        Socket a(3);
        Socket b(4);
        a = std::move(b);
        check(socket_close_calls == 1, "move-assignment releases the old handle");
    }
    check(socket_close_calls == 2,
          "chain closes twice: assignment and final destruction");
}

static void test_parse_int(void) {
    check(parse_int("42").value_or(-1) == 42, "parse_int reads a value");
    check(!parse_int("abc").has_value(), "parse_int reports invalid text");
    check(!parse_int("9999999999999999999999").has_value(),
          "parse_int reports out of range");
    check(!parse_int("").has_value(), "parse_int reports empty input");
}

static void test_counter(void) {
    counter.store(0, std::memory_order_relaxed);
    std::vector<std::thread> threads;
    for (int t = 0; t < 8; t++) {
        threads.emplace_back([]() {
            for (int i = 0; i < 1000; i++) {
                inc();
            }
        });
    }
    for (auto& t : threads) {
        t.join();
    }
    check(counter.load() == 8000, "atomic counter counts every increment");
}

static void test_add_locked(void) {
    {
        std::lock_guard<std::mutex> guard(mu);
        data.clear();
    }
    std::vector<std::thread> threads;
    for (int t = 0; t < 8; t++) {
        threads.emplace_back([]() {
            for (int i = 0; i < 250; i++) {
                add(1);
            }
        });
    }
    for (auto& t : threads) {
        t.join();
    }
    check(data.size() == 2000, "guarded vector holds every push");
}

static void test_build_bounds(void) {
    std::vector<int> small = build(3);
    check(small.size() == 3 && small[2] == 2, "build fills positive counts");
    check(build(0).empty(), "build accepts zero");
    bool rejected = false;
    try {
        build(-1);
    } catch (const std::invalid_argument&) {
        rejected = true;
    }
    check(rejected, "build rejects negative counts explicitly");
}

int main(void) {
    test_make_foo();
    test_open_file();
    test_views();
    test_make_task();
    test_buffer();
    test_socket_moves();
    test_parse_int();
    test_counter();
    test_add_locked();
    test_build_bounds();
    printf("%s\n", failures ? "FAILURES" : "ALL-OK");
    return failures ? 1 : 0;
}
