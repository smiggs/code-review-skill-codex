// Support prelude for the extracted C++ guide units. The extracted fence
// bytes are never modified; this prelude supplies includes and stubs whose
// behaviour the tests set up per case. Force-include this with
// `-include cpp-prelude.hpp` when compiling the combined units+tests file.
#pragma once
#include <atomic>
#include <cstddef>
#include <cstdio>
#include <functional>
#include <memory>
#include <mutex>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <vector>
#include <thread>

inline bool foo_init_succeeds = true;
struct Foo {
    bool Init() { return foo_init_succeeds; }
};

inline std::string make_name_value = "codex";
inline std::string make_name() { return make_name_value; }

inline void use(int) {}

inline int socket_close_calls = 0;
inline void socket_close_stub(int) { ++socket_close_calls; }
/* The extracted Socket fence calls unqualified close(fd_); redirect it to
 * the recording stub without touching the extracted bytes. */
#define close socket_close_stub
