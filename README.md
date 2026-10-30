# Calculus Learning Lab v1.9 — PRE-RELEASE (local testing only)

This builds on v1.8 and retains three calculators, graphs, guided solutions and practice exercises.

## Run

```powershell
py -m pip install -r requirements.txt
py -m unittest discover -v
py -m streamlit run app.py
```

## What's new
- A separate spawned process performs a **preflight** symbolic computation with a 6-second timeout. The UI does not proceed if this check fails.
- Updated release status and warnings so users do not mistake this for a production-safe app.
- Added worker tests and a release checklist.

## Known limitations / blockers
- **Not ready for public deployment.** The UI still repeats some symbolic operations, constructs worked steps, renders graphs and checks practice answers in-process, without complete memory/time isolation. Preflight is not a substitute for guarding all computation.
- Preflight performs duplicate calculation and can increase latency.
- No independent hosting isolation, concurrency/load tests, or comprehensive edge-case validation.
- No user accounts or permanent progress storage.
- Selected symbolic methods may lack full derivations.

See `RELEASE_CHECKLIST.md` for acceptance criteria. Do not use Streamlit's Deploy button yet.


See README_V2_5.md for new integral application practice topics.
