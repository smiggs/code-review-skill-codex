# Synthetic consumer requirements

The event log is append-only. Recording an event must preserve every existing
event and append the new event with one trailing newline. The writer accepts a
path to a UTF-8 text file and a single-line event.

Review the change from `writer-before.py` to `writer-after.py` against that
requirement. These rules belong only to this synthetic consumer. Review requests
authorise analysis, not fixes or external review submission.
