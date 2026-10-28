# Common Bugs Checklist

Language-specific bugs and issues to watch for during code review.

Use patterns in this inherited guide as inspection prompts under the
[review contract](review-contract.md), not as findings or fixed severity rules.
Confirm the target's versions, caller behaviour, trigger, and impact. The
[reference status](reference-status.md) records unaudited framework examples.
Missing tests, an external test dependency, or a familiar pattern alone is not
proof of a defect.

## Universal Issues

### Logic Errors
- [ ] Off-by-one errors in loops and array access
- [ ] Incorrect boolean logic (De Morgan's law violations)
- [ ] Missing null/undefined checks
- [ ] Race conditions in concurrent code
- [ ] Incorrect comparison operators (== vs ===, = vs ==)
- [ ] Integer overflow/underflow
- [ ] Floating point comparison issues

### Resource Management
- [ ] Memory leaks (unclosed connections, listeners)
- [ ] File handles not closed
- [ ] Database connections not released
- [ ] Event listeners not removed
- [ ] Timers/intervals not cleared

### Error Handling
- [ ] Swallowed exceptions (empty catch blocks)
- [ ] Generic exception handling hiding specific errors
- [ ] Missing error propagation
- [ ] Incorrect error types thrown
- [ ] Missing finally/cleanup blocks

## TypeScript/JavaScript

Use the [TypeScript and JavaScript guide](typescript.md) for runtime validation,
indexed access, shared mutation, and promise ownership. Trace the consumer and
failure path: assertions do not validate JSON, `void` does not consume rejection,
and cancellation does not by itself prevent every stale continuation.
Propagating rejection to an awaiting caller and using `Promise.all` for required
results are valid controls. Compiler strictness and lint preferences need the
target project's configuration; they are not universal defect criteria.

### React

Use the [React guide](react.md) for Hooks, effects, identity, actions, Suspense,
and server/client boundaries. Confirm React, React DOM, framework, and query
library versions separately. Inspect stale result/error publication, unintended
state resets, form ownership, and actual recovery boundaries. Conditional child
rendering, React 19's conditional `use`, explicit loading state, inline callbacks,
and a client wrapper receiving server-rendered children can be valid controls.
Memoisation, boundary placement, and cache defaults need demonstrated impact.

## Vue 3

Use the [Vue guide](vue.md) for reactive inputs, compiler-sensitive props
transformations, watcher ownership, and lifecycle cleanup. Trace whether a
consumer needs a live value or an intentional snapshot. Inspect overlapping
request success, error, and loading writes and the exact listener target cleaned
up. Vue 3.5 reactive props destructuring is distinct from ordinary object
destructuring. Getter inputs, explicit prop/update pairs, `withDefaults`, and
non-virtual lists can be valid controls; missing type-only declarations or newer
API adoption alone do not establish defects.

## Python

Use the [Python review guide](python.md) for checked examples and version limits.
Inspect shared mutable defaults or class state, swallowed failures, resource
cleanup, exhausted iterators, cancellation, and input boundaries where relevant.
Intentional sharing and broad boundary handlers need their actual contracts;
string concatenation or missing annotations alone do not establish defects.

## Rust

### 所有权与借用

```rust
// ❌ Use after move
let s = String::from("hello");
let s2 = s;
println!("{}", s);  // Error: s was moved

// ✅ Clone if needed (but consider if clone is necessary)
let s = String::from("hello");
let s2 = s.clone();
println!("{}", s);  // OK

// ❌ 用 clone() 绕过借用检查器（反模式）
fn process(data: &Data) {
    let owned = data.clone();  // 不必要的 clone
    do_something(owned);
}

// ✅ 正确使用借用
fn process(data: &Data) {
    do_something(data);  // 传递引用
}

// ❌ 在结构体中存储借用（通常是坏主意）
struct Parser<'a> {
    input: &'a str,  // 生命周期复杂化
    position: usize,
}

// ✅ 使用拥有的数据
struct Parser {
    input: String,  // 拥有数据，简化生命周期
    position: usize,
}

// ❌ 迭代时修改集合
let mut vec = vec![1, 2, 3];
for item in &vec {
    vec.push(*item);  // Error: cannot borrow as mutable
}

// ✅ 收集到新集合
let vec = vec![1, 2, 3];
let new_vec: Vec<_> = vec.iter().map(|x| x * 2).collect();
```

### Unsafe 代码审查

```rust
// ❌ unsafe 没有安全注释
unsafe {
    ptr::write(dest, value);
}

// ✅ 必须有 SAFETY 注释说明不变量
// SAFETY: dest 指针由 Vec::as_mut_ptr() 获得，保证：
// 1. 指针有效且已对齐
// 2. 目标内存未被其他引用借用
// 3. 写入不会超出分配的容量
unsafe {
    ptr::write(dest, value);
}

// ❌ unsafe fn 没有 # Safety 文档
pub unsafe fn from_raw_parts(ptr: *mut T, len: usize) -> Self { ... }

// ✅ 必须文档化安全契约
/// Creates a new instance from raw parts.
///
/// # Safety
///
/// - `ptr` must have been allocated via `GlobalAlloc`
/// - `len` must be less than or equal to the allocated capacity
/// - The caller must ensure no other references to the memory exist
pub unsafe fn from_raw_parts(ptr: *mut T, len: usize) -> Self { ... }

// ❌ 跨模块 unsafe 不变量
mod a {
    pub fn set_flag() { FLAG = true; }  // 安全代码影响 unsafe
}
mod b {
    pub unsafe fn do_thing() {
        if FLAG { /* assumes FLAG means something */ }
    }
}

// ✅ 将 unsafe 边界封装在单一模块
mod safe_wrapper {
    // 所有 unsafe 逻辑在一个模块内
    // 对外提供 safe API
}
```

### 异步/并发

```rust
// ❌ 在异步上下文中阻塞
async fn bad_fetch(url: &str) -> Result<String> {
    let resp = reqwest::blocking::get(url)?;  // 阻塞整个运行时！
    Ok(resp.text()?)
}

// ✅ 使用异步版本
async fn good_fetch(url: &str) -> Result<String> {
    let resp = reqwest::get(url).await?;
    Ok(resp.text().await?)
}

// ❌ 跨 .await 持有 Mutex
async fn bad_lock(mutex: &Mutex<Data>) {
    let guard = mutex.lock().unwrap();
    some_async_op().await;  // 持锁跨越 await！
    drop(guard);
}

// ✅ 缩短锁持有时间
async fn good_lock(mutex: &Mutex<Data>) {
    let data = {
        let guard = mutex.lock().unwrap();
        guard.clone()  // 获取数据后立即释放锁
    };
    some_async_op().await;
    // 处理 data
}

// ❌ 在异步函数中使用 std::sync::Mutex
async fn bad_async_mutex(mutex: &std::sync::Mutex<Data>) {
    let _guard = mutex.lock().unwrap();  // 可能死锁
    tokio::time::sleep(Duration::from_secs(1)).await;
}

// ✅ 使用 tokio::sync::Mutex（如果必须跨 await）
async fn good_async_mutex(mutex: &tokio::sync::Mutex<Data>) {
    let _guard = mutex.lock().await;
    tokio::time::sleep(Duration::from_secs(1)).await;
}

// ❌ 忘记 Future 是惰性的
fn bad_spawn() {
    let future = async_operation();  // 没有执行！
    // future 被丢弃，什么都没发生
}

// ✅ 必须 await 或 spawn
async fn good_spawn() {
    async_operation().await;  // 执行
    // 或
    tokio::spawn(async_operation());  // 后台执行
}

// ❌ spawn 任务缺少 'static
async fn bad_spawn_lifetime(data: &str) {
    tokio::spawn(async {
        println!("{}", data);  // Error: data 不是 'static
    });
}

// ✅ 使用 move 或 Arc
async fn good_spawn_lifetime(data: String) {
    tokio::spawn(async move {
        println!("{}", data);  // OK: 拥有数据
    });
}
```

### 错误处理

```rust
// ❌ 生产代码中使用 unwrap/expect
fn bad_parse(input: &str) -> i32 {
    input.parse().unwrap()  // panic!
}

// ✅ 正确传播错误
fn good_parse(input: &str) -> Result<i32, ParseIntError> {
    input.parse()
}

// ❌ 吞掉错误信息
fn bad_error_handling() -> Result<()> {
    match operation() {
        Ok(v) => Ok(v),
        Err(_) => Err(anyhow!("operation failed"))  // 丢失原始错误
    }
}

// ✅ 使用 context 添加上下文
fn good_error_handling() -> Result<()> {
    operation().context("failed to perform operation")?;
    Ok(())
}

// ❌ 库代码使用 anyhow（应该用 thiserror）
// lib.rs
pub fn parse_config(path: &str) -> anyhow::Result<Config> {
    // 调用者无法区分错误类型
}

// ✅ 库代码用 thiserror 定义错误类型
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("failed to read config file: {0}")]
    Io(#[from] std::io::Error),
    #[error("invalid config format: {0}")]
    Parse(#[from] serde_json::Error),
}

pub fn parse_config(path: &str) -> Result<Config, ConfigError> {
    // 调用者可以 match 不同错误
}

// ❌ 忽略 must_use 返回值
fn bad_ignore_result() {
    some_fallible_operation();  // 警告：unused Result
}

// ✅ 显式处理或标记忽略
fn good_handle_result() {
    let _ = some_fallible_operation();  // 显式忽略
    // 或
    some_fallible_operation().ok();  // 转换为 Option
}
```

### 性能陷阱

```rust
// ❌ 不必要的 collect
fn bad_process(items: &[i32]) -> i32 {
    items.iter()
        .filter(|x| **x > 0)
        .collect::<Vec<_>>()  // 不必要的分配
        .iter()
        .sum()
}

// ✅ 惰性迭代
fn good_process(items: &[i32]) -> i32 {
    items.iter()
        .filter(|x| **x > 0)
        .sum()
}

// ❌ 循环中重复分配
fn bad_loop() -> String {
    let mut result = String::new();
    for i in 0..1000 {
        result = result + &i.to_string();  // 每次迭代都重新分配！
    }
    result
}

// ✅ 预分配或使用 push_str
fn good_loop() -> String {
    let mut result = String::with_capacity(4000);  // 预分配
    for i in 0..1000 {
        write!(result, "{}", i).unwrap();  // 原地追加
    }
    result
}

// ❌ 过度使用 clone
fn bad_clone(data: &HashMap<String, Vec<u8>>) -> Vec<u8> {
    data.get("key").cloned().unwrap_or_default()
}

// ✅ 返回引用或使用 Cow
fn good_ref(data: &HashMap<String, Vec<u8>>) -> &[u8] {
    data.get("key").map(|v| v.as_slice()).unwrap_or(&[])
}

// ❌ 大结构体按值传递
fn bad_pass(data: LargeStruct) { ... }  // 拷贝整个结构体

// ✅ 传递引用
fn good_pass(data: &LargeStruct) { ... }

// ❌ Box<dyn Trait> 用于小型已知类型
fn bad_trait_object() -> Box<dyn Iterator<Item = i32>> {
    Box::new(vec![1, 2, 3].into_iter())
}

// ✅ 使用 impl Trait
fn good_impl_trait() -> impl Iterator<Item = i32> {
    vec![1, 2, 3].into_iter()
}

// ❌ retain 比 filter+collect 慢（某些场景）
vec.retain(|x| x.is_valid());  // O(n) 但常数因子大

// ✅ 如果不需要原地修改，考虑 filter
let vec: Vec<_> = vec.into_iter().filter(|x| x.is_valid()).collect();
```

### 生命周期与引用

```rust
// ❌ 返回局部变量的引用
fn bad_return_ref() -> &str {
    let s = String::from("hello");
    &s  // Error: s will be dropped
}

// ✅ 返回拥有的数据或静态引用
fn good_return_owned() -> String {
    String::from("hello")
}

// ❌ 生命周期过度泛化
fn bad_lifetime<'a, 'b>(x: &'a str, y: &'b str) -> &'a str {
    x  // 'b 没有被使用
}

// ✅ 简化生命周期
fn good_lifetime(x: &str, _y: &str) -> &str {
    x  // 编译器自动推断
}

// ❌ 结构体持有多个相关引用但生命周期独立
struct Bad<'a, 'b> {
    name: &'a str,
    data: &'b [u8],  // 通常应该是同一个生命周期
}

// ✅ 相关数据使用相同生命周期
struct Good<'a> {
    name: &'a str,
    data: &'a [u8],
}
```

### Rust 审查清单

**所有权与借用**
- [ ] clone() 是有意为之，不是绕过借用检查器
- [ ] 避免在结构体中存储借用（除非必要）
- [ ] Rc/Arc 使用合理，没有隐藏不必要的共享状态
- [ ] 没有不必要的 RefCell（运行时检查 vs 编译时）

**Unsafe 代码**
- [ ] 每个 unsafe 块有 SAFETY 注释
- [ ] unsafe fn 有 # Safety 文档
- [ ] 安全不变量被清晰记录
- [ ] unsafe 边界尽可能小

**异步/并发**
- [ ] 没有在异步上下文中阻塞
- [ ] 没有跨 .await 持有 std::sync 锁
- [ ] spawn 的任务满足 'static 约束
- [ ] Future 被正确 await 或 spawn
- [ ] 锁的顺序一致（避免死锁）

**错误处理**
- [ ] 库代码使用 thiserror，应用代码使用 anyhow
- [ ] 错误有足够的上下文信息
- [ ] 没有在生产代码中 unwrap/expect
- [ ] must_use 返回值被正确处理

**性能**
- [ ] 避免不必要的 collect()
- [ ] 大数据结构传引用
- [ ] 字符串拼接使用 String::with_capacity 或 write!
- [ ] impl Trait 优于 Box<dyn Trait>（当可能时）

**类型系统**
- [ ] 善用 newtype 模式增加类型安全
- [ ] 枚举穷尽匹配（没有 _ 通配符隐藏新变体）
- [ ] 生命周期尽可能简化

## SQL

### Injection Vulnerabilities
```sql
-- ❌ String concatenation (SQL injection risk)
query = "SELECT * FROM users WHERE id = " + user_id

-- ✅ Parameterized queries
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### Performance Issues
- [ ] Missing indexes on filtered/joined columns
- [ ] SELECT * instead of specific columns
- [ ] N+1 query patterns
- [ ] Missing LIMIT on large tables
- [ ] Inefficient subqueries vs JOINs

### Common Mistakes
- [ ] Not handling NULL comparisons correctly
- [ ] Missing transactions for related operations
- [ ] Incorrect JOIN types
- [ ] Case sensitivity issues
- [ ] Date/timezone handling errors

## API Design

### REST Issues
- [ ] Inconsistent resource naming
- [ ] Wrong HTTP methods (POST for idempotent operations)
- [ ] Missing pagination for list endpoints
- [ ] Incorrect status codes
- [ ] Missing rate limiting

### Data Validation
- [ ] Missing input validation
- [ ] Incorrect data type validation
- [ ] Missing length/range checks
- [ ] Not sanitizing user input
- [ ] Trusting client-side validation

## Testing

### Test Quality Issues
- [ ] Testing implementation details instead of behavior
- [ ] Missing edge case tests
- [ ] Flaky tests (non-deterministic)
- [ ] Tests with external dependencies
- [ ] Missing negative tests (error cases)
- [ ] Overly complex test setup
