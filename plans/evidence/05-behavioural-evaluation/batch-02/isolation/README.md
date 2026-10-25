# Evaluator context preflight

On 25 October 2026, local CLI `0.164.0-alpha.11.1` rendered two case-free
contexts with `debug prompt-input`. No model call, authentication attempt,
review, or subagent dispatch occurred. The first render used defaults; the
second used the proposed evaluation settings.

The process ran under `/tmp/review-isolation-preflight-7b9pyl9x`, outside this
repository, with a newly created Codex home. The inherited environment was
limited to `PATH`, `HOME`, `LANG`, and `CODEX_HOME`. The user's home value was
preserved; the Codex home was separate and initially empty. No credentials or
user configuration were copied. Temporary paths may not survive; recreate
them and inspect again before execution.

## Saved evidence

- [Default command](command.json), [context](prompt-input.json), and
  [stderr](stderr.txt).
- [Configured command](configured-command.json),
  [context](configured-prompt-input.json), and [stderr](configured-stderr.txt).
- [CLI version](version.txt), [exec help](exec-help.txt), and
  [context renderer help](prompt-input-help.txt).

Both commands exited zero. Both warned that helper binaries could not be
created under a temporary Codex home; context rendering still succeeded.
Whether execution needs those helpers remains untested.

Manual inspection found no repository `AGENTS.md`, installed review skill,
review contract, answer key, criteria, prior report, or parent conversation.
User messages contain only the temporary environment and the case-free
inspection request. The configured permissions name only `scratch` as writable,
with restricted network access and no approval escalation. This is rendered
configuration, not a test of OS enforcement or a read-access boundary.

Ordinary Codex developer guidance and four bundled system-skill listings
remain: imagegen, openai-docs, skill-creator, and skill-installer. No personal
review or house-style skills are listed. These shared defaults must be
disclosed and equivalent in both arms; the proposal does not claim a model
without global instructions. Tool schemas include orchestration and
collaboration tools, but the batch proposal permits no delegation.

## Recheck before review

Recreate the temporary layout and environment shown in the configured command.
Run its case-free render from `scratch` before adding a fixture. Inspect all
messages and tool schemas, not only a marker search. After preparing one
case/arm, render its exact evaluator prompt and inspect again. Candidate and
input are siblings of scratch, outside its writable root. Do not disable
instruction discovery: target requirements must remain readable from input.

Use the same settings for the eventual standalone `exec` invocation. Preserve
the actual session's initial messages and traces before accepting an independence
result. A matching local debug render reduces the known injection risk; it
does not establish authentication, model availability, actual execution
context, or useful review behaviour. Stop and record unresolved if those
requirements cannot be verified. Do not silently fall back to this chat.

## Official documentation consulted

The official [instruction discovery guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
describes global and project instruction discovery and a separate Codex home.
The [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents the sandbox options used here. The
[non-interactive guide](https://learn.chatgpt.com/docs/non-interactive-mode)
documents JSON events and fresh CLI execution. The installed CLI's saved help
establishes availability of the local context renderer. These sources informed
the setup; the raw local renders establish the observed context contents.
