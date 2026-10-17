# Security review guide

Use this guide for a requested security audit or a concrete trust boundary affected
by a change. Establish assets, actors, supported configurations, and scope under
the [review contract](review-contract.md). See the
[reference status](reference-status.md) for the limits of this guide's audit.

## Trace authority and data

Follow untrusted input to the operation it controls. Identify authentication,
resource authorisation, tenancy, privileged actions, and sensitive outputs.
An authenticated user can still lack permission for a particular object or action;
check the target's access rules and failure behaviour. Public endpoints do not
inherently require authentication. See the
[OWASP authorisation guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).

Inspect token verification, session handling, and reset flows against the actual
identity system's contract and installed library version. Do not treat a copied
JWT configuration or a particular access-control model as universally secure.
A missing defence is a finding only with an evidenced exposure or violated
requirement; unexplored defence-in-depth ideas remain suggestions or questions.

## Input and execution boundaries

Inspect SQL parameters, command arguments, rendered output, filesystem paths,
redirects, and outbound requests where those sinks are reachable. Determine the
applicable escaping, validation, and authorisation mechanism from the target API.
A "sanitise input" instruction without a sink-specific contract is insufficient.

Avoid constructing shell commands from untrusted text. A direct executable launch
with separate arguments removes ordinary shell parsing, but attacker-controlled
arguments may still become executable options. Validate executable selection and
program-specific arguments. Platform behaviour matters, including Windows batch
files. See [OWASP command injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)
and [Python subprocess security](https://docs.python.org/3.10/library/subprocess.html#security-considerations).

For paths, compare resolved path components rather than textual prefixes. Account
for traversal, symlinks, and concurrent replacement according to the threat model.
Taking a basename alone neither establishes authorisation nor prevents name
collisions. See the bounded [Python path example](python.md) for a stable-tree
case; it does not claim race-free hostile filesystem access.

## Sensitive state and availability

Inspect reachable secret exposure in source, logs, errors, responses, build output,
and configuration. Determine the target's encryption, retention, and deletion
requirements rather than asserting a legal conclusion. Do not copy real secret
values into a report; cite the location and describe the exposure.

For dependencies, verify the affected installed version, reachable vulnerable
behaviour, and authoritative advisory before claiming a vulnerability. Do not
invent advisory identifiers or infer safety from a clean scanner result.

For availability, establish supported resource bounds, request sizes, timeouts,
retry behaviour, and abuse paths. Rate limiting, lockout, and validation rules
need the system's requirements and threat model; their mere absence does not
assign a severity.

## Evidence, severity, and authority

For each finding, identify attacker capability, input, affected asset, observable
impact, and the path establishing reachability. Use a safe reproduction or static
trace; do not run an exploit, export sensitive material, or mutate a live service
as an evaluation side effect. If essential configuration or reachability is unknown,
record a material question.

Map urgency and impact to the contract's P0–P3 labels or explain the project's
severity mapping. A conditional exposure can still be urgent. Confidence and
unverified assumptions stay separate. A security recommendation does not approve,
block, or merge changes through an external service; target human approvals remain
required. Use the [report template](../assets/pr-review-template.md).
