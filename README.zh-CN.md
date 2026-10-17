[English](./README.md) | [简体中文](./README.zh-CN.md)

# 适用于 Codex 的 Code Review Skill

参考来源：https://github.com/awesome-skills/code-review-skill

本分支正在准备对 NefelibataBIGR/code-review-skill-codex 进行适配。
[上游基线与文件清单](plans/evidence/01-upstream-inventory.md)记录来源及保留的 MIT 许可证。
[审查约定](reference/review-contract.md)已于 2026 年 10 月 18 日获用户批准。
工作包 02 的入口和模板已合并到 `main`。工作包 03 限定范围内的 Python 和专题指南变更已于 2026 年 10 月 18 日获用户批准；
[参考指南状态](reference/reference-status.md)记录已核验的范围与暂缓的技术检查。
改写后的指南、约定和验证记录仅提供英文版本。
此处说明的是当前工作分支，而非下方安装命令克隆的上游版本。

这是一个面向 Codex 的模块化 skill，用来把代码审查变成更结构化、信息密度更高的工作流。

它支持多语言仓库中的 PR、补丁和本地变更审查，并将架构审计和安全审计作为显式模式。

## 仓库内容

- `SKILL.md`：skill 主入口和触发元数据
- `agents/openai.yaml`：Codex UI 元数据
- `reference/`：按需加载的语言和专题审查指南
- `assets/`：可复用模板与检查清单
- `scripts/`：辅助脚本，包括 PR 分析工具

## 支持的审查范围

- React
- Vue
- TypeScript
- Python
- Java
- Go
- Rust
- C
- C++
- CSS / Less / Sass
- Qt
- 架构审查
- 性能审查
- 安全审查
- 常见 Bug 模式检查

## Codex 如何使用这个 Skill

Codex 通过 [SKILL.md](./SKILL.md) 中的元数据发现这个 skill。触发描述刻意只强调“什么时候该加载”：

- 审查 pull request
- 审查代码变更
- 做架构审查
- 做安全审查
- 对补丁或本地变更输出结构化审查意见

没有审查任务的实现或调试请求不应触发此 skill。

skill 被加载后，Codex 会优先按需读取 `reference/` 下的文件，而不是一次把所有内容都塞进上下文。

## 安装

### 全局安装

把这个仓库克隆或复制到 Codex skills 目录：

```bash
# macOS / Linux
git clone https://github.com/NefelibataBIGR/code-review-skill-codex.git \
  ~/.codex/skills/code-review-codex

# Windows PowerShell
git clone https://github.com/NefelibataBIGR/code-review-skill-codex.git `
  "$env:USERPROFILE\.codex\skills\code-review-codex"
```

### 备用位置

如果你的环境偏向个人 agent skills，也可以复制到：

```bash
~/.agents/skills/code-review-codex
```

安装后需要重启 Codex，让新的 skill 元数据生效。

## 使用方式

### 显式调用

直接在提示词里引用 skill：

```text
Use code-review-codex to review this PR.
Focus on supported bugs, regressions, and violated requirements.
```

### 自然语言触发

这个 skill 也支持通过普通请求自然触发，例如：

```text
Review these changes for bugs and maintainability issues.
```

```text
Do an architecture review of this refactor.
```

```text
Check this service for security problems before merge.
```

## 审查风格

这个 skill 适合以下类型的 review：

- 优先查找 bug、回归和违反要求的问题，而非个人偏好。
- 每条问题都提供精确位置、触发条件、影响和证据。
- 将优先级与置信程度分开，将待确认问题与已证实问题分开。
- 允许没有可执行问题的结果，并说明范围和验证限制。
- 仅在相关时读取语言或专题指南。

审查请求仅授权分析和建议报告。修改代码、发布评论或审查、批准以及合并都需要单独授权，
并遵守目标项目的人工批准要求。[报告模板](assets/pr-review-template.md)采用问题优先的格式。
检查与变更有关的架构或安全影响，不会自动扩展为全系统审计。

## 仓库结构

```text
code-review-codex/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- reference/
|   |-- reference-status.md
|   |-- review-contract.md
|   |-- react.md
|   |-- vue.md
|   |-- typescript.md
|   |-- python.md
|   |-- java.md
|   |-- go.md
|   |-- rust.md
|   |-- c.md
|   |-- cpp.md
|   |-- qt.md
|   |-- css-less-sass.md
|   |-- architecture-review-guide.md
|   |-- performance-review-guide.md
|   |-- security-review-guide.md
|   |-- common-bugs-checklist.md
|   `-- code-review-best-practices.md
|-- assets/
|   |-- review-checklist.md
|   `-- pr-review-template.md
`-- scripts/
    `-- pr-analyzer.py
```

## 维护说明

- `SKILL.md` 只保留触发条件和核心流程，不堆砌大段参考资料。
- 详细模式和最佳实践放进 `reference/`。
- 安装或使用方式变化时，同时更新中英文文档。
- 示例尽量贴近真实代码审查场景。

贡献和验证说明见 [CONTRIBUTING.zh-CN.md](./CONTRIBUTING.zh-CN.md)。
