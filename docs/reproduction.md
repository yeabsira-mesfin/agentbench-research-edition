# Reproduction

Use Linux/macOS with Python 3.12+ and Node 22+. No paid API or external dataset is needed. Review the bundled candidates before executing.

```bash
npm --prefix frontend ci --ignore-scripts
python -m pip install -r backend/requirements.txt
RUN_TRUSTED_FIXTURES=1 python -m unittest discover -s tests -v
PYTHONPATH=backend python -m pytest backend/tests -q
python -m research.runner --repeats 1
npm run build
npm --prefix frontend run preview
```

Open the Vite preview URL. Research results are bundled; the reviewer workbench also requires the original FastAPI service. `npm run dev` expects that API at localhost:8000 unless `VITE_API_BASE_URL` is set.

JSON and CSV are written to `frontend/public/data/benchmark.*`. Input hashes and category outcomes reproduce; timestamps, runtime/platform metadata and durations legitimately vary. `--task`, `--candidate`, `--repeats` (1–10) and `--label` permit controlled comparisons. Unknown task/candidate values are rejected. Changing fixtures requires an explicit manifest/hash update after code review.
