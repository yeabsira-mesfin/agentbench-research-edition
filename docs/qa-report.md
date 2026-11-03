# QA report

Verified locally on 2026-11-03 with Python 3.12.14 and Node 24.22.1.

- Six runner tests passed: reference/fault discrimination, input rejection, hash mismatch, infrastructure classification, constrained replacement, repeated-input integrity.
- Eight original FastAPI/evaluator tests passed. One dependency deprecation warning was emitted by Starlette's HTTPX adapter.
- Vite production build and TypeScript check passed.
- One-repeat end-to-end sample: 9 candidates / 57 assertions; 3 reference candidates pass all gates, 3 deliberate security-fault controls fail security, 3 regression controls fail regression. Designed fixture failures are experimental outcomes, not failed harness tests.
- No arbitrary submitted code was executed. No secrets required. Fixture-only limits are explicitly not a sandbox claim.
- GitHub Actions and new Vercel deployment are checked separately after publication; local success does not establish remote CI or deployment success.
