# Package 06: documentation and distribution

Status: candidate prepared and checked; human distribution approval pending.
[Package 06 evidence](evidence/06-documentation-and-distribution.md) records the
manifest-pinned working candidate, completed checks, and remaining limits.
The user accepted package 05's
[completion exceptions](evidence/05-completion-and-exceptions.md) on 25 October
2026. This removes the package dependency; it does not approve a release or
publication.

## Outcome

Make the adapted skill installable and maintainable with honest capability
claims, preserved attribution, and a recorded verified revision.

## Deliverables and responsibilities

- Update README and contribution guidance around the final implemented scope.
  Explain differences from upstream and identify unverified reference areas.
- Align shared installation and usage instructions in the existing Chinese
  companions; document translation limitations rather than pretending parity.
- Preserve MIT notices, upstream links, and authorship provenance. Distinguish
  upstream material from local adaptations without inventing a new licence.
- Document installation from a pinned commit into the user's supported skills
  location, including scripts and references. Use actual verified tool behaviour
  for reload instructions rather than copying assumptions from upstream.
- Provide an optional upload archive for ChatGPT surfaces that support custom
  skills. Verify required structure; do not claim availability in every ChatGPT
  product or account without checking its supported capability.
- Exclude Git metadata, private evaluation artefacts, caches, credentials, and
  unnecessary development files from any distributed archive.
- In an isolated skill location, check explicit invocation, ordinary review
  discovery, reference resolution, and operation without optional integrations.
- Record release candidate revision, validation commands, evaluation results,
  known limitations, and update/rollback instructions.
- Disclose the accepted severity-calibration limitation and incomplete upstream
  comparison in capability claims and release evidence. Do not claim that the
  original evaluation criteria all passed or that the adaptation is superior.
- Keep push, tags, public release publication, and live PR comments as distinct
  actions requiring user authorisation, not implicit results of packaging.

## Verification

Inspect the built archive's file list and unpack it into a fresh temporary
directory. Run structural checks and a representative behavioural fixture from
that copy. Confirm bundled reference paths and any retained helper work without
the development checkout.

## Human checkpoint

Review installation instructions, upstream divergence, supported environments,
and evaluation evidence. Approve a release candidate before any requested
publication; record the exact revision and outstanding limitations.

## Exit criteria

- Distribution contains the complete usable skill and required licence notices.
- Installation and representative review work from the distributed copy.
- Documentation reflects measured behaviour and known limitations.
- Publication and installation state are reported accurately and separately.
