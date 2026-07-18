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


## 2026-07-14

- Suppression de la dependance C amont `cryptacular` de l'environnement de
  CI (elle n'etait pas epinglee : pip compilait silencieusement le sdist
  1.6.2). La reecriture drop-in maintenue (`michaellaunay/cryptacular` 2.x,
  backends bcrypt PyCA + hashlib, compatible hash pour hash avec le module
  deploye) est installee depuis son depot a la place ; `bcrypt`, `cffi` et
  `pycparser` epingles pour la cible Python 3.6.


## 2026-07-16

- Documentation de phase 2 de daceui, livrée en une passe
  (1 507 lignes) : document de conception `architecture.md` (EN/FR) et
  `usage-scenarios.md` (EN/FR), plus une passe de docstrings complète —
  86 docstrings après lecture intégrale, `tools/doc_coverage.py`
  ajouté. Couverture : 1,0 % → 88,8 % (6/6 modules, 36/36 classes,
  45/56 fonctions ; résidu : constructeurs et surcharges triviales,
  conformément à la politique annoncée).
- Savoirs fixés par écrit : daceui est la console d'administration du
  moteur *construite comme des processus dace* (cinq définitions
  `isUnique`, discriminateur `DaceManager` — le moteur se gère avec
  lui-même) ; `DaceUIAPI` est le service ajax des panneaux d'actions
  que les applications hôtes consomment (collecter → rendre → exécuter
  l'action postée → **rejouer** tout le panneau pour ne jamais montrer
  un état périmé) ; la surcharge `request.ajax_api` est le moyen pour
  un hôte de pointer les rappels du panneau vers son propre endpoint ;
  les actions de départ virtuelles sont re-résolues depuis le triplet
  (pd, nœud, behavior) ; un processus sans work-items compte comme
  *bloqué* dans les tableaux de bord. L'orthographe historique
  `action_infomrations` est conservée et documentée (la renommer est un
  changement d'API de phase 3).


## 16/07/2026 — Phase 3 / M3

- **daceui est vert sur Python 3.12 : 6 tests, 0 échec, 0 erreur — et
  ce sont ses tout premiers tests** (la CI historique ne faisait qu'un
  smoke d'import). La suite est de niveau smoke mais de bout en bout :
  les cinq définitions DaceManager de la console s'enregistrent,
  l'utilitaire ``dace_ui_api`` se résout, ``calculatePage`` pagine,
  ``update_actions`` rend un panneau complet (collecter → rendre →
  assembler), la surcharge ``request.ajax_api`` re-pointe les URL de
  rappel, et un test HTTP se connecte à la SDI et rend
  ``/runtime/@@index`` — la console auto-hébergée vivante sur
  Chameleon 4.
- **Zéro modification du code du paquet** : le portage n'a demandé que
  le harnais et les tests. La propreté de la phase 2 plus le socle
  M1/M2 (réacteur asyncio, shims deform 3, ``tm.annotate_user``) ont
  porté daceui par héritage.
- Une leçon pour les hôtes (note M4) : pontus et daceui déclarent
  chacun un layout pyramid_layout *par défaut* — inclusions sœurs à
  égalité, pyramid lève ``ConfigurationConflictError`` ; l'application
  doit enregistrer son propre layout pour posséder l'arbitrage,
  exactement comme nova-ideo le fait.
- Emballage bi-pile calqué sur M1/M2 : `constraints-modern.txt`, tox
  `py312`, job CI `py312-tests` (dace et pontus installés depuis git
  d'abord), job legacy épinglé sur `legacy-golden-master`, extra
  `test` (WebTest), version 2.0.0.dev0. Le buildout de KuneAgi
  épingle déjà daceui au SHA certifié.

- Correctif attrapé par la CI : l'ajout M3 d'`extras_require`
  doublonnait le mot-clé préexistant de `setup.py` — une `SyntaxError`
  au build que la vérification du jalon avait manquée, `compileall`
  couvrant le paquet mais pas le `setup.py` à la racine. Fusion en un
  extra unique (`test=['WebTest']` ; la couche robot historique
  `pyramid_robot` est inutilisée par la suite). Règle de vérification
  étendue : `setup.py` lui-même est compilé.

- **Rafraîchissement documentaire.** Le README énonce la réalité
  bi-pile et la toute première suite ; CHANGES gagne l'entrée du
  correctif `extras_require` ; l'architecture gagne la section du
  harnais de tests (et la leçon du layout par défaut).

- **T3 : les vues console et l'endpoint JSON sont épinglés** — 8 tests
  sur le harnais M3. Couverture : util.py **56 % → 76 %**, views.py
  **54 % → 72 %**, total daceui **67 % → 81 %** ; suite 14/14.
  Épinglés : les cinq vues console côté définitions rendent
  (marqueurs, dont l'identifiant de template historique
  `panel-RutimeStat`) ; `action_infomrations` sous ses deux visages
  (app fraîche : actions sans oid → branche START, urls adressées par
  le triplet (pd, nœud, behavior) ; après qu'un rendu console les a
  instanciées → branche OID, urls par `action_uid`) ;
  `get_action_body` répond une Structure de layout non vide (variante
  ressources incluse) ; `statistic_dates` agrège à la minute. Le
  contrat d'erreur ASYMÉTRIQUE de l'endpoint JSON est épinglé : les
  chemins de résolution gardés répondent `{}` (op absent/inconnu,
  uids bidons), mais le rendu ne l'est pas — une action start
  recalculée d'un triplet valide résout, sa vue refuse, et pontus fait
  surface en HTTPInternalServerError ; le chemin `action_uid` rend le
  corps.

- **Pause documentaire.** Le README porte la réalité des 14 tests et
  les chiffres de couverture ; CHANGES gagne l'entrée T3 consolidée.

- **Fenêtre des renommages.** `action_infomrations` →
  `action_informations` (méthode — rien de persisté ; la coquille
  demeure en alias de compatibilité, gardé par un test) et
  `panel-RutimeStat` → `panel-RuntimeStat` dans les deux gabarits de
  statistiques ; les tests T3 retournés en conséquence.
