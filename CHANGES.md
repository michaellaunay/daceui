# Changelog

## Unreleased

### Fork maintenance — 2026-07-13 (`michaellaunay/daceui`)

- Repository forked from `ecreall/daceui`; maintenance resumed by Michaël Launay (Logikascium). Ecréall's intellectual property was acquired by Logikascium in 2024; license unchanged (AGPL v3+).
- `README.rst` and `CHANGES.rst` converted to Markdown (`README.md`, `CHANGES.md`); README rewritten with the repository status, legacy requirements and the modernisation roadmap.
- Build metadata updated: fork URLs, maintainer field, Markdown `long_description`, Python 3.6 classifier; minimal `pyproject.toml` added (PEP 518 `[build-system]` only — metadata stays in `setup.py` until the Phase 3 packaging migration); `MANIFEST.in` updated for Markdown files.
- Buildout `sources.cfg` repaired: the dead `git://` protocol (disabled by GitHub in 2022) replaced by `https://`; `dace` and `pontus` sources repointed to their maintained forks (`michaellaunay/dace`, `michaellaunay/pontus`).
- Added `constraints-legacy.txt` (known-good 2017 dependency pins extracted from nova-ideo's `versions.cfg`) and a best-effort GitHub Actions workflow (`python:3.6-buster` container, `ecreall_dace` and `ecreall_pontus` installed from their maintained forks, import smoke check — the test suite is currently empty; to be stabilised in Phase 1).
- `.gitignore` extended from the start to exclude delivery artifacts (patches, diffs, archives) and `git apply` leftovers.
- Bilingual documentation structure added (`docs/en/`, `docs/fr/`), including the worklog / fil de l'eau and the documentation policy (`docs/README.md`).

### Planned (modernisation roadmap → 2.0.0)

- Phase 1: reproducible legacy build + green CI (golden master).
- Phase 2: exhaustive documentation (docstrings, UI/behaviour rendering protocol shared with DaCE and Pontus) and the first characterisation tests.
- Phase 3, after DaCE 2.0 and Pontus 2.0: Python 3.12, Pyramid 2.x; maintained substanced fork; first real pytest suite; PEP 621 packaging with `uv`; ruff; gradual typing; retirement of the buildout files. Module dotted names frozen to preserve ZODB pickles.

### Inherited unreleased changes (upstream `1.0.5.dev`, 2017–2018)

- No entries were recorded upstream for this version; the repository nevertheless contains changes committed until 2018-12-21 (last upstream commit: "add processes").

## 1.0.4 — 2017-02-25

- Fix in the jquery.infinitescroll.js file to trigger the event locally.

## 1.0.3 — 2017-01-06

- Add include_resources parameter to the different view methods.

## 1.0.2 — 2016-09-15

- Fix dace ui api.

## 1.0.1 — 2016-08-18

- Include mo files in the release.

## 1.0 — 2016-06-28

- Initial version.
