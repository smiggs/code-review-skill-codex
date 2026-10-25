# Package 12: CSS, Less, and Sass

Status: planned; implementation and technical verification have not begun.

## Outcome

Provide evidence-based review guidance for styling behaviour, accessibility
requirements, and browser and preprocessor compatibility.

Apply the [package 03 approach](03-python-and-reference-quality.md) to [css-less-sass.md](../reference/css-less-sass.md).
Follow the [shared audit requirements](README.md#language-audit-requirements).

## Deliverables and responsibilities

- Audit cascade, specificity, inheritance, custom properties, layout,
  overflow, responsive behaviour, and supported browser features.
- Verify Less and Sass examples against the chosen implementation and version;
  distinguish preprocessor constructs from native CSS behaviour.
- Replace automatic severity for transitions, shadows, selectors, and layout
  properties with reproducible rendering or performance consequences.
- Respect project design tokens, breakpoints, naming, and compatibility policy.
  Avoid treating important declarations, nesting depth, or fixed dimensions
  as defects without a violated requirement or concrete failure.
- Test relevant keyboard focus, zoom, reduced motion, and content expansion
  requirements. Record the applicable accessibility expectations explicitly.
- Reconcile remaining technical advice with the scoped policy corrections
  already recorded in package 03.
- Rewrite scoped guidance in concise British English, preserve existing paths
  and attribution, and reconcile corresponding common-bug checklist sections.
- Update the reference disposition with verified scope and remaining limits.
  Record corrections, sources, checks, and upstream divergence in a package
  evidence record when implementation produces evidence.

## Tests and verification

Compile retained Less and Sass examples with pinned implementations. Use
small browser fixtures for cascade, layout, responsive boundaries, and any
retained accessibility claims. Record browser versions, viewport conditions,
and actual assertions; screenshots alone do not establish interaction behaviour.
Performance findings need a stated workload and measured effect. Include valid
important declarations and fixed-size controls to check false positives.

Run the shared documentation and structural checks. Record commands, versions,
results, and unavailable checks; do not equate example tests with review accuracy.
Prepare known-defect fixtures and clean controls for a separate, agreed
[behavioural evaluation](05-behavioural-evaluation.md).

## Human checkpoint

Review the technical corrections, supported versions, retained scope, and
translation limits. Record approval or outstanding work against the exact
revision. Behavioural evaluation acceptance remains a separate decision.

## Exit criteria

- Scoped guidance is concise, version-aware, and consistent with the contract.
- Retained technical claims have primary-source support and meaningful examples
  have recorded checks or explicitly accepted validation limits.
- No tool preference, style rule, or performance pattern alone becomes a defect.
- Guide routing and related checklist advice agree; relative links work.
- The evidence record states corrections, deferred work, and the human decision.
- Any claim of evaluated review accuracy cites a separate accepted evaluation;
  this technical audit does not itself complete package 05 or authorise release.
