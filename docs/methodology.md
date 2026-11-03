# Methodology

Research question: which failures escape visible correctness checks but are exposed by separately specified security and regression tests?

Three deterministic Python microtasks operationalize tenant isolation, SQL literal handling, and filesystem containment. SEC-411 and DB-307 adapt concepts from the existing six-task reviewer catalog; FILE-101 adds a file-security task. These are Python adaptations, not executable equivalents of every original task or language.

Every task has a baseline, a reference, a deliberately unsafe control, a regression control, test code, expected outcomes, a version and SHA-256 hashes. Candidate provenance is synthetic and locally controlled. Labels are descriptive user metadata, not evidence that an AI model generated a solution.

The runner validates task/candidate IDs and hashes, copies a baseline to a disposable directory, applies a single allowlisted replacement to `solution.py`, and runs visible, security and regression groups in separate child processes. Tests are independent assertions for different properties, but public and visible to candidate authors. There are no secret holdouts; test leakage and manual benchmark construction limit external validity.

Report per-category test pass counts and run failure counts. A release gate passes only if all groups pass. Build/import failures, infrastructure errors, timeout/resource events and assertion failures are separate statuses. Infrastructure cases are excluded from ordinary pass/failure denominators. Maintainability is a long-line warning only, not a validated quality score.

Repeats verify execution consistency; they are not independent samples. Timings include process startup, vary across machines, and should not be interpreted as application performance. No inference about real coding agents is supported by these nine controls.
