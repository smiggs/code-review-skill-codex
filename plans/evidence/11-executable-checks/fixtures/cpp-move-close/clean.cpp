#include <cstddef>
#include <cstdio>
#include <map>
#include <utility>

/* Connection registry counting every open and close of each handle. */
static std::map<int, int> g_closes;
static int g_next_handle = 100;

static int open_reg(void) { return g_next_handle++; }
static void close_reg(int handle) { ++g_closes[handle]; }

/* Owns a registry handle; moving transfers ownership and resets the source. */
class Conn {
public:
    Conn() : handle_(open_reg()) {}
    ~Conn() {
        if (handle_ >= 0) {
            close_reg(handle_);
        }
    }

    Conn(Conn&& other) noexcept : handle_(std::exchange(other.handle_, -1)) {}
    Conn& operator=(Conn&& other) noexcept {
        if (this != &other) {
            if (handle_ >= 0) {
                close_reg(handle_);
            }
            handle_ = std::exchange(other.handle_, -1);
        }
        return *this;
    }

private:
    int handle_;
};

int main() {
    {
        Conn outer;
        {
            Conn inner = std::move(outer);
            (void)inner;
        }
    }
    int total = 0;
    for (const auto& entry : g_closes) {
        total += entry.second;
        std::printf("handle %d closed %d times\n", entry.first, entry.second);
    }
    std::printf("closes=%d\n", total);
    return 0;
}
