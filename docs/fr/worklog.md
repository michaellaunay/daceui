# Fil de l'eau

Journal au fil de l'eau des travaux sur ce dépôt, du plus récent au plus ancien.
English version: [`../en/worklog.md`](../en/worklog.md).

## 2026-07-13

- Fork de `ecreall/daceui` vers `michaellaunay/daceui` ; reprise de la
  maintenance par Michaël Launay (Logikascium).
- Conversion de `README.rst` et `CHANGES.rst` en Markdown ; README réécrit avec
  le statut du dépôt et la feuille de route de modernisation.
- Mise à jour des métadonnées de build (`setup.py` : URLs du fork, champ
  mainteneur, description longue en Markdown, classifieur Python 3.6) ; ajout
  d'un `pyproject.toml` minimal (PEP 518) ; mise à jour du `MANIFEST.in`.
- Réparation du `sources.cfg` buildout : protocole `git://` mort remplacé par
  `https://` ; `dace` et `pontus` repointés vers leurs forks maintenus.
- Ajout de `constraints-legacy.txt` et d'un workflow de CI legacy best-effort
  (`python:3.6-buster` ; `ecreall_dace` et `ecreall_pontus` installés depuis
  leurs forks ; test d'import — la suite de tests est vide à ce jour).
- Exclusion d'origine des artefacts de livraison (`*.patch`, `*.diff`,
  archives) et des résidus de `git apply` via `.gitignore`.
- Mise en place de la structure de documentation bilingue (`docs/en`,
  `docs/fr`) et de ce fil de l'eau.
- Restauration des changements de maintenance du fork : le commit initial
  (477b1f8) ne contenait que le fichier de patch de livraison, *non
  appliqué* — la commande d'application référençait
  `../daceui-fork-maj.patch` alors que le fichier avait été enregistré dans
  le dépôt ; la chaîne `&&` s'est arrêtée au `--check` et le fichier orphelin
  a été commité seul. Le contenu du patch est désormais appliqué et le
  fichier orphelin supprimé (et ignoré à l'avenir).
- Application préventive des correctifs d'époque validés par les runs de
  dace et pontus : `setuptools<46` (les sdists de 2016/2017 utilisent l'API
  `Feature` supprimée dans setuptools 46), apt repointé vers
  archive.debian.org (buster archivée en 2024), `libzmq3-dev` (pyzmq 14.4.1
  via ecreall_dace, sans wheel Python 3.6), `libjpeg-dev`/`zlib1g-dev`
  (Pillow 3.4.2 via ecreall_pontus, même raison), `actions/checkout` passé
  en v5. `mock` n'est volontairement pas ajouté : avec une suite de tests
  vide, aucun Configurator Pyramid n'est créé, donc le scan venusian de
  substanced ne s'exécute jamais.
