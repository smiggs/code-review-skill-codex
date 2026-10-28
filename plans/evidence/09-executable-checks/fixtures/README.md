# Prepared Go and Rust fixtures

These synthetic, distributable fixtures supply one defective `head` and a clean
`base` for each language. Each base is copied from the retained guide example;
the Go head adapts the inherited algorithm to a complete callback API. The Rust
head deliberately discards progress between calls. They need the corresponding
harness module and declared contracts to compile and exercise them.

For a future independent review, provide only the selected base/head diff,
necessary module metadata, and the following target requirements:

- Go: positive worker counts are required even for empty input. Non-positive
  counts must return an error promptly. Parent cancellation must reach active
  callbacks; every worker must finish before the pool returns. Callbacks are
  concurrent-safe and cooperate with cancellation.
- Rust: after a frame read is cancelled, the same reader and frame-state object
  must resume the incomplete four-byte frame without losing consumed bytes.
  Completed calls must advance to the next frame.

The [answer key](answer-key.md), test sources, sensitivity logs, and audit
narrative must be withheld from the reviewer. Agree review prompts, isolation,
scoring, severity expectations, and acceptance criteria before any model runs.
No such evaluation has been run or accepted for package 09.
