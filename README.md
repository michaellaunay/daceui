# DaceUI (`ecreall_daceui`)

DaceUI provides the reusable UI parts for the [DaCE](https://github.com/michaellaunay/dace) workflow engine: Pyramid views, panels and Chameleon templates used to render and drive DaCE processes (process actions, state and history) in host applications. It sits on top of [Pontus](https://github.com/michaellaunay/pontus) for view composition and forms.

The repository also ships a minimal standalone Pyramid application (`paste.app_factory` entry point, `development.ini`, buildout configuration) for developing the components in isolation.

## Repository status

This repository is a **maintained fork** of [`ecreall/daceui`](https://github.com/ecreall/daceui) (original development by Ecréall, 2014–2018), forked in July 2026 and maintained by Michaël Launay ([Logikascium](https://github.com/michaellaunay)). Ecréall's intellectual property was acquired by Logikascium in 2024; the license is unchanged: **AGPL v3+**.

This fork is part of the modernisation effort of the [Nova-Ideo](https://github.com/ecreall/nova-ideo) / [KuneAgi](https://github.com/ecreall/KuneAgi) participatory-innovation platform. The `master` branch currently reflects the **legacy state** of the library (Python 3.6-era stack); see the [roadmap](#roadmap--planned-updates) below and `CHANGES.md`.

## Current requirements (legacy)

- Python 3.6 — the modernisation targets Python 3.12
- `ecreall_dace` and `ecreall_pontus` (use the maintained forks: [`michaellaunay/dace`](https://github.com/michaellaunay/dace), [`michaellaunay/pontus`](https://github.com/michaellaunay/pontus)), `pyramid_chameleon`, `pyramid_layout`, substanced 1.0a1, waitress
- Known-good dependency pins are provided in [`constraints-legacy.txt`](constraints-legacy.txt), extracted from the historical nova-ideo `versions.cfg` (the last environment in which the whole stack was known to work together)
- The buildout `sources.cfg` has been repaired on this fork: the dead `git://` protocol was replaced by `https://`, and `dace`/`pontus` now point to their maintained forks

## Installation

Add `ecreall_daceui` to `install_requires` in your `setup.py`, then edit `production.ini` in your Pyramid application:

```ini
pyramid.includes =
    ...
    daceui
```

For an isolated legacy development environment:

```bash
python3.6 -m pip install -c constraints-legacy.txt \
    "git+https://github.com/michaellaunay/dace.git#egg=ecreall_dace" \
    "git+https://github.com/michaellaunay/pontus.git#egg=ecreall_pontus" \
    -e .
```

## Running the tests

The test suite is **currently empty** — writing the first tests is a roadmap item (Phases 2–3). Until then, the CI performs an import smoke check plus the (empty) historical suite:

```bash
python -c "import daceui"
python setup.py test
```

A best-effort GitHub Actions workflow ([`.github/workflows/tests.yml`](.github/workflows/tests.yml)) runs this inside a `python:3.6-buster` container, installing `ecreall_dace` and `ecreall_pontus` from their maintained forks. It will be stabilised during Phase 1 of the roadmap (reproducible legacy build).

## Documentation

Documentation lives in [`docs/`](docs/):

- [`docs/en/`](docs/en/) — primary documentation, in English
- [`docs/fr/`](docs/fr/) — documentation in French

Audits, design documents and the worklog are maintained in both languages. See [`docs/README.md`](docs/README.md) for the documentation policy.

Design documents: [architecture](docs/en/architecture.md) · [usage scenarios](docs/en/usage-scenarios.md) (English originals; French mirrors under [`docs/fr/`](docs/fr/)).

## Used by

- [nova-ideo](https://github.com/ecreall/nova-ideo) and its variant [KuneAgi](https://github.com/ecreall/KuneAgi)
- [l'agenda commun](https://github.com/ecreall/lagendacommun)

## Roadmap — planned updates

The plan follows the Nova-Ideo modernisation audit (Logikascium, July 2026):

1. **Phase 1 — Reproducible legacy build ("golden master").** Frozen environment and green CI; for DaceUI, whose own suite is empty, non-regression relies on the nova-ideo functional suite plus the import smoke check.
2. **Phase 2 — Exhaustive documentation.** Docstring pass over the package, documentation of the UI/behaviour rendering protocol shared with DaCE and Pontus, and the **first characterisation tests**.
3. **Phase 3 — Modernisation (target: version 2.0.0).** Ported **after** DaCE 2.0 and Pontus 2.0 (bottom-up dependency order):
   - Port to Python 3.12; Pyramid 2.x
   - Move from the abandoned substanced 1.0a1 to the maintained, trimmed-down fork
   - First real pytest suite; packaging to PEP 621 (`pyproject.toml`) with `uv`; ruff linting; gradual typing
   - Retirement of the buildout files (`buildout.cfg`, `sources.cfg`, …) in favour of the standard toolchain
   - Python module names (dotted paths) are **frozen** to preserve existing ZODB pickles

Versioning: `1.0.x` = legacy maintenance on this fork; `2.0.0` = the modernised library.

## Translations

This product has been translated into: French.

## Contribute

- Issue tracker: <https://github.com/michaellaunay/daceui/issues>
- Source code: <https://github.com/michaellaunay/daceui>
- Historical upstream: <https://github.com/ecreall/daceui>

## License

The project is licensed under the AGPL v3 or later (AGPLv3+). See [`LICENSE`](LICENSE).
