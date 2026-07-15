# daceui — scénarios d'utilisation

*Compagnon de [`architecture.md`](architecture.md). English version: [`../en/usage-scenarios.md`](../en/usage-scenarios.md).*

## Scénario 1 — Câbler, ou lancer en autonome

```ini
pyramid.includes =
    substanced
    pyramid_layout
    dace
    pontus
    daceui
```

`includeme` scanne le paquet (les cinq définitions `DaceManager` s'enregistrent) et monte `daceuistatic`. Autre voie : `daceui.main` est une application WSGI complète — pointez-lui un `zodbconn.uri` et vous obtenez la console d'administration du moteur, seule.

## Scénario 2 — Rendre un panneau d'actions (le motif nova-ideo)

```python
from pyramid.threadlocal import get_current_registry
from daceui.interfaces import IDaceUIAPI

dace_ui_api = get_current_registry().getUtility(IDaceUIAPI, 'dace_ui_api')
all_actions = dace_ui_api.get_actions([proposal], self.request,
                                      process_or_id=process)
action_updated, messages, resources, actions = \
    dace_ui_api.update_actions(self.request, all_actions)
```

Chaque entrée d'`actions` porte le corps encodé JSON de la vue de l'action, un id composé stable, les URL ajax `actionurl_update` / `actionurl_after` et `assigned_to` — tout ce qu'un template doit savoir pour rendre un panneau d'actions. Si le POST visait l'un des formulaires, ce behavior s'est exécuté et l'ensemble a été **rejoué** (revalidé, re-rendu) : les corps retournés reflètent l'état post-exécution. `messages` peut porter l'erreur « Action non realisee » (droit perdu entre-temps, ou verrou dace détenu).

## Scénario 3 — Pointer les rappels vers votre propre endpoint

```python
request.ajax_api = '@@my-ajax-api'      # avant de construire le panneau
```

`updateaction_viewurl`/`afterexecution_viewurl` l'honorent ; votre vue répond alors à `op=update_action` (retourner le corps rafraîchi d'une action — `DaceUIAPIJson.update_action` montre comment, y compris le cas de l'action de départ virtuelle reconstruite depuis `pd_id`/`action_id`/`behavior_id`) et à `op=after_execution_action` (le rappel de déverrouillage déclenché quand un formulaire de panneau est abandonné).

## Scénario 4 — Les écrans de la console

Sur un site en marche, en Admin : `<racine>/runtime/@@Processes` liste les instances (un processus sans work-items apparaît *bloqué*), `@@StatisticRun` le tableau de bord dygraph ; `<racine>/process_definition_container/@@ProcessesDef` groupe les définitions par discriminateur ; sur un processus, `@@Process` montre les actions de sa définition, `@@lesdonneesmanipulees` les entités de son contexte d'exécution (courantes vs historique), `@@actionsrealiser` les actions en attente sur les impliqués actifs. Les tables se paginent par les paramètres `page<tabid>`/`number<tabid>` (7 lignes par défaut).

## Scénario 5 — Assigner une activité ou une action

Sur une `IActivity` : `@@assign_activity` ; sur une `IBusinessAction` : `@@assign_action` (assignés actuels + le formulaire Select2). Les deux exécutent `set_assignment` via les behaviors d'`activity_pd` — l'assignation alimente ensuite le pipeline `validate_action` de dace (une action assignée ne valide que pour ses assignés).
