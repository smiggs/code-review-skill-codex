# Local installation decision

On 26 October 2026, the user instructed: "install the skill on this machine".
This authorises the local installation below. It does not record approval of
package 06's distribution checkpoint, a committed release, or publication.

Installed 31 files from the checked local `dist/code-review-codex.zip` into
`/home/andrew/.agents/skills/code-review-codex`. The destination did not exist;
no existing skill was overwritten. No personal configuration was changed.

Archive SHA-256:
`b10c6838941cad407a9fd1382f02316d346c3b48558bc1edbaaf4995e319e3eb`.
Every installed file matches the [candidate manifest](06-distribution/manifest.json).
Archive integrity, path boundaries, and exact file inventory were checked before
copying; all 31 installed hashes were verified afterwards. The repository
structural validator passed against the personal installation, using pinned
PyYAML 6.0.3. This does not repeat the candidate's behavioural smoke checks.

The skill should be available on the next turn. If it does not appear, restart
Codex. Use `code-review-codex` explicitly to distinguish this adaptation from the
separately installed `code-review` skill.
