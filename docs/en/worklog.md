# Worklog

Running log of the work on this repository, newest first.
Version française : [`../fr/worklog.md`](../fr/worklog.md).

## 2026-07-13

- Forked `ecreall/daceui` to `michaellaunay/daceui`; maintenance resumed by
  Michaël Launay (Logikascium).
- Converted `README.rst` and `CHANGES.rst` to Markdown; rewrote the README
  with the repository status and the modernisation roadmap.
- Updated build metadata (`setup.py`: fork URLs, maintainer field, Markdown
  long description, Python 3.6 classifier); added a minimal PEP 518
  `pyproject.toml`; updated `MANIFEST.in`.
- Repaired the buildout `sources.cfg`: dead `git://` protocol replaced by
  `https://`; `dace` and `pontus` repointed to their maintained forks.
- Added `constraints-legacy.txt` and a best-effort legacy CI workflow
  (`python:3.6-buster`; `ecreall_dace` and `ecreall_pontus` installed from
  their forks; import smoke check — the test suite is currently empty).
- Ignored delivery artifacts (`*.patch`, `*.diff`, archives) and `git apply`
  leftovers in `.gitignore` from the start.
- Established the bilingual documentation structure (`docs/en`, `docs/fr`)
  and this worklog.
- Restored the fork-maintenance changes: the initial commit (477b1f8)
  contained only the *unapplied* delivery patch file — the apply command
  referenced `../daceui-fork-maj.patch` while the file had been saved inside
  the repository, so the `&&` chain stopped at `--check` and the stray file
  was committed alone. The patch content is now applied and the stray file
  removed (and ignored from now on).
- Preventively applied the era-compatibility fixes proven by dace's and
  pontus' CI runs: `setuptools<46` (the 2016/2017 sdists still use the
  `Feature` API removed in setuptools 46), apt repointed to
  archive.debian.org (buster archived in 2024), `libzmq3-dev` (pyzmq 14.4.1
  via ecreall_dace has no Python 3.6 wheel), `libjpeg-dev`/`zlib1g-dev`
  (Pillow 3.4.2 via ecreall_pontus, same reason), `actions/checkout` bumped
  to v5. `mock` is deliberately not added: with an empty test suite no
  Pyramid Configurator is created, so substanced's venusian scan never runs.


## 2026-07-14

- Removed the dead upstream `cryptacular` C dependency from the CI
  environment (it was never pinned: pip was silently building the 1.6.2
  sdist). The maintained drop-in rewrite (`michaellaunay/cryptacular` 2.x,
  PyCA bcrypt + hashlib backends, hash-compatible with the deployed module)
  is installed from its repository instead; `bcrypt`, `cffi` and `pycparser`
  pinned for the Python 3.6 target.


## 2026-07-16

- Phase 2 documentation of daceui, delivered in one pass (1,507 lines):
  design document `architecture.md` (EN/FR) and `usage-scenarios.md`
  (EN/FR), plus a full docstring pass — 86 docstrings from a complete
  read, `tools/doc_coverage.py` added. Coverage: 1.0 % → 88.8 %
  (6/6 modules, 36/36 classes, 45/56 functions; residue: constructors
  and trivial overrides, per the stated policy).
- Knowledge fixed in writing: daceui is the engine's administration
  console *built as dace processes* (five `isUnique` definitions,
  discriminator `DaceManager` — the engine manages itself with
  itself); `DaceUIAPI` is the ajax action-panel service the host
  applications consume (collect → render → execute the posted one →
  **replay** the whole panel so it never shows a stale state); the
  `request.ajax_api` override is how a host points the panel callbacks
  at its own endpoint; virtual start actions are re-resolved from the
  (pd, node, behavior) triple; a process without work-items counts as
  *blocked* in the dashboards. The historical `action_infomrations`
  spelling is kept and documented (renaming is a Phase-3 API change).
