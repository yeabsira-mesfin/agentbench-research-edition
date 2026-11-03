# Limitations and safety

- No arbitrary upload, external patch path, model API or public execution endpoint is supported.
- The hash manifest is an integrity check against accidental change, not an authenticity boundary against a repository editor who changes both source and hash. Review fixture code before running it.
- POSIX subprocesses receive a scrubbed environment, temporary working directory, isolated Python import mode, CPU/memory/open-file/process/file-size limits, wall timeout and bounded logs. The same host user is used. Host filesystem and network isolation are NOT enforced. This is suitable only for trusted fixtures.
- A verified microVM or equivalent hardened sandbox with non-root identity, network denial, filesystem isolation, credentials isolation and externally enforced resource controls is required before arbitrary untrusted execution can be enabled. Ordinary Docker alone is not asserted to satisfy this.
- Tests are small, public, synthetic and Python-only. No real model performance, held-out benchmark validity, broad language coverage or maintainability model is claimed.
- Results are checked-in snapshots, with no server persistence or live execution from the dashboard.
- The original deployment remains in `agentbench-swe`; new Vercel deployment is separate.
