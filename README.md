# AgentBench Research Edition

**When does a candidate pass basic correctness yet fail security or regression checks?**

An executable research extension of [AgentBench SWE](https://github.com/yeabsira-mesfin/agentbench-swe), with the original React reviewer workbench and FastAPI scoring API preserved. The original deployment is not changed. This repository was repurposed from an earlier JavaScript learning repository. Its unrelated practice files have been removed from the current tree; earlier versions remain accessible in Git history.

## What works

- Three versioned Python tasks: tenant authorization, parameterized SQLite search, and contained path resolution.
- Nine synthetic candidate runs: reference, security-fault, and regression controls per task.
- Fresh disposable directories, constrained single-file replacements, fixture hashes, separate test categories, exit codes, timings, bounded logs, and JSON/CSV export.
- React research dashboard with task/candidate filters, comparison tables, pass-count charts, expandable evidence, and original reviewer workbench.
- Existing `/health`, `/evaluate`, `/api/tasks`, `/api/evaluate` API contracts retained.

**Arbitrary untrusted patches are disabled.** A POSIX subprocess is not a malicious-code sandbox. Only the reviewed, bundled fixtures are supported; no model-generated candidate provenance is invented.

## Run

```bash
# Python 3.12+, Node 22+
npm --prefix frontend ci --ignore-scripts
npm run dev
# In a second terminal, optional original reviewer API:
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --port 8000
# Generate executable evidence:
python -m research.runner --repeats 2
# Dashboard consumes frontend/public/data/benchmark.json
```

```bash
RUN_TRUSTED_FIXTURES=1 python -m unittest discover -s tests -v
PYTHONPATH=backend python -m pytest backend/tests -q
npm run build
```

The committed one-repeat example contains **9 real executions of synthetic candidates**: all 3 reference implementations pass every gate; all 3 security-fault implementations pass visible correctness and fail security. Across 57 individual checks, 43 pass and 14 fail as designed. These counts validate the harness, not real AI model performance.

## Reproduce and deploy

See [reproduction](docs/reproduction.md), [Vercel setup](docs/deployment.md), [architecture](docs/architecture.md), [methodology](docs/methodology.md), [limitations](docs/limitations.md), and [QA](docs/qa-report.md). Root `vercel.json` retains upstream Vite + FastAPI multi-service routing. No Vercel deployment is claimed by this repository's local QA.

## Original contribution and related projects

This adds executable evidence to the existing reviewer-attested scoring application. It is an independent small benchmark, not the unrelated AgentBench academic benchmark and not a peer-reviewed evaluation.

- [Dependency Health Observatory](https://github.com/yeabsira-mesfin/React)
- [Post-Merge Maintenance Study](https://github.com/yeabsira-mesfin/React-)

Upstream source snapshot: `agentbench-swe@6738f3c15ea9495fda5da55c4ada29e1d9febd64`. The prior README is retained at [upstream-readme](docs/upstream-readme.md). MIT license applies to the owner's software in this research edition. No third-party datasets or paper implementations were copied.
