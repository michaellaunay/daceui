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


## 2026-07-16 — Phase 3 / M3

- **daceui is green on Python 3.12: 6 tests, 0 failures, 0 errors —
  and they are its first tests ever** (the historical CI only
  import-smoked). The suite is smoke-level but end to end: the five
  DaceManager console definitions register, the ``dace_ui_api``
  utility resolves, ``calculatePage`` paginates, ``update_actions``
  renders a full panel (collect → render → assemble), the
  ``request.ajax_api`` override re-points the callback URLs, and an
  HTTP test logs into the SDI and renders ``/runtime/@@index`` — the
  self-hosting console alive on Chameleon 4.
- **Zero changes to the package code**: the port needed only the
  harness and the tests. Phase-2 cleanliness plus the M1/M2 groundwork
  (asyncio reactor, deform-3 shims, ``tm.annotate_user``) carried
  daceui by inheritance.
- One lesson for hosts (M4 note): pontus and daceui both declare a
  *default* pyramid_layout — sibling includes tie and pyramid raises a
  ``ConfigurationConflictError``; the application must register its
  own layout to own the tie-break, exactly as nova-ideo does.
- Dual-stack packaging mirrored from M1/M2: `constraints-modern.txt`,
  tox `py312`, CI `py312-tests` job (dace and pontus installed from
  git first), legacy job pinned to `legacy-golden-master`, a `test`
  extra (WebTest), version 2.0.0.dev0. KuneAgi's buildout already pins
  daceui at the certified SHA.

- CI-caught fixup: the M3 `extras_require` addition duplicated the
  pre-existing keyword in `setup.py` — a build-time `SyntaxError` the
  milestone verification missed because `compileall` covered the
  package, not the repo-root `setup.py`. Merged into a single extra
  (`test=['WebTest']`; the historical `pyramid_robot` robot layer is
  unused by the suite). Verification rule extended: `setup.py` itself
  is compiled.

- **Documentation refresh.** README states the dual-stack reality and
  the first-ever suite; CHANGES gains the `extras_require` fix entry;
  architecture gains the test-harness section (and the default-layout
  lesson).

- **T3: the console views and the JSON endpoint are pinned** — 8 tests
  on the M3 harness. Coverage: util.py **56 % → 76 %**, views.py
  **54 % → 72 %**, daceui total **67 % → 81 %**; suite 14/14. Pinned:
  the five definition-side console views render (markers, including
  the historical `panel-RutimeStat` template id); `action_infomrations`
  under both faces (fresh app: oid-less actions → START branch, urls
  addressed by the (pd, node, behavior) triple; after a console render
  instantiates them → OID branch, urls by `action_uid`);
  `get_action_body` answers a truthy layout Structure (resources
  variant included); `statistic_dates` buckets by minute. The JSON
  endpoint's ASYMMETRIC error contract is pinned: guarded resolution
  paths answer `{}` (missing/unknown op, bogus uids), but rendering is
  unguarded — a start action recomputed from a valid triple resolves,
  its view refuses, and pontus surfaces HTTPInternalServerError; the
  `action_uid` path renders the body.

- **Documentation pause.** README carries the 14-test reality and the
  coverage figures; CHANGES gains the consolidated T3 entry.
