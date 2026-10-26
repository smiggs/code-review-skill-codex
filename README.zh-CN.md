[English](./README.md) | [简体中文](./README.zh-CN.md)

# Codex 代码审查技能

`code-review-codex` 审查拉取请求、补丁和本地变更，寻找有证据支持的缺陷、回归和需求违背。
架构与安全审计需要明确范围。可使用本地文件或已有连接工具，不依赖 CodeRabbit、
GitHub CLI 或特定 MCP 服务。可选统计脚本需要 Python 3.10 或更高版本。

本适配源自 [NefelibataBIGR/code-review-skill-codex](https://github.com/NefelibataBIGR/code-review-skill-codex)，
其注明更早来源为 [awesome-skills/code-review-skill](https://github.com/awesome-skills/code-review-skill)。
保留原始版权声明与 [MIT 许可证](LICENSE)。基线、改动和来源核查限制见
[来源与验证范围](reference/provenance.md)。

## 行为与限制

[入口](SKILL.md) 按需加载参考指南，[审查约定](reference/review-contract.md)规定证据与权限边界。
每个问题应包含位置、触发条件、影响和证据；疑问与建议分开，无可操作问题也是有效结果。
审查请求只授权分析和建议报告，修复、提交、发布审查、批准和合并需要单独授权及目标项目批准。

Python 与部分专题指南已完成限定范围核查。React、Vue、TypeScript、Rust、Java、Go、C、C++、
Qt、CSS/Less/Sass 及继承的常见错误示例仍有技术核查待办。请先阅读
[参考指南状态](reference/reference-status.md)。重写的运行指导为英文，中文文档对齐安装、使用和贡献步骤，
但未完成技术全文翻译或双语验证。

已接受的合成评估发现四个预置缺陷，误报为零，但四个优先级只匹配三个：一个约定为 P1 的问题被报为 P0。
严重性仍需人工判断。一次上游运行未生成报告，因此比较不完整，不能据此声称优于上游。
原始验收标准并未全部通过，也不能推断其他语言、生产仓库、大型差异或重复运行的准确性。
详情见[验证摘要](reference/provenance.md#verification)。

## 固定提交安装

以下命令针对 Linux，需要 Git 和 Python 3.10 或更高版本。请从人工批准的候选记录选择完整提交 ID。
`APPROVED_COMMIT` 是占位符，不是已发布版本。工作包 06 候选仍待人工检查，本次工作未发布版本。

```bash
git clone https://github.com/smiggs/code-review-skill-codex.git /tmp/code-review-source
git -C /tmp/code-review-source checkout --detach APPROVED_COMMIT
git -C /tmp/code-review-source rev-parse HEAD
```

确认输出与所选 ID 一致后，在该检出目录按照[分发与安装指南](reference/distribution.md)构建并检查白名单 ZIP，
然后解压到 `~/.agents/skills`。完整包包含 `reference/`、`assets/`、`agents/`、
`scripts/pr-analyzer.py` 和 `LICENSE`，不能只复制 `SKILL.md`。避免在多个扫描位置安装同名技能。

[OpenAI 官方指导](https://learn.chatgpt.com/docs/build-skills)（2026 年 10 月 25 日查阅）
列出的个人位置为 `~/.agents/skills`，仓库位置为 `.agents/skills`。
Codex 自动检测技能变化；若未显示，再重启。CLI 或 IDE 可用 `/skills` 或 `$code-review-codex` 选择。
这些是文档说明，不代表本项目已测试所有客户端；实际环境见候选证据。

## 使用

显式调用：

```text
Use code-review-codex to review these changes for supported bugs, regressions, and violated requirements.
```

普通审查请求：

```text
Review these changes for bugs and regressions.
```

提供补丁或仓库及比较范围。技能读取项目需求，调查具体故障路径，优先输出问题并说明实际检查和限制。
没有审查任务的实现或调试请求不在触发范围内。

可选[差异统计工具](reference/helper-tooling.md)仅提供文件数和文本行数，不输出风险分数或批准建议，
无需第三方 Python 包；仍受其 Git 差异输入契约限制。

## 分发与维护

[分发指南](reference/distribution.md)提供包内容、安装、更新、回退和有条件的 ChatGPT 上传说明。
ZIP 是独立技能目录，不是插件，也不是所有 ChatGPT 界面都支持的附件。需核实具体界面和账户的导入及执行支持；
本次没有执行上传。指南以英文为准，尚无完整中文翻译。

贡献与检查见[贡献说明](CONTRIBUTING.zh-CN.md)。完整计划和评估记录位于源码仓库的 `plans/`，不进入安装包。
