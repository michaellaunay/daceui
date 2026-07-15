# daceui — usage scenarios

*Companion to [`architecture.md`](architecture.md). French version: [`../fr/usage-scenarios.md`](../fr/usage-scenarios.md).*

## Scenario 1 — Wire in, or run standalone

```ini
pyramid.includes =
    substanced
    pyramid_layout
    dace
    pontus
    daceui
```

`includeme` scans the package (the five `DaceManager` definitions register themselves) and mounts `daceuistatic`. Alternatively, `daceui.main` is a complete WSGI application: point a `zodbconn.uri` at it and you get the engine administration console alone.

## Scenario 2 — Render an actions panel (the nova-ideo pattern)

```python
from pyramid.threadlocal import get_current_registry
from daceui.interfaces import IDaceUIAPI

dace_ui_api = get_current_registry().getUtility(IDaceUIAPI, 'dace_ui_api')
all_actions = dace_ui_api.get_actions([proposal], self.request,
                                      process_or_id=process)
action_updated, messages, resources, actions = \
    dace_ui_api.update_actions(self.request, all_actions)
```

Each entry of `actions` carries the JSON-encoded body of the action's view, a stable composed id, the `actionurl_update` / `actionurl_after` ajax URLs and `assigned_to` — everything a template needs to render an action panel. When the POST targeted one of the forms, that behaviour executed and the whole set was **replayed** (re-validated, re-rendered): the returned bodies reflect the post-execution state. `messages` may carry the "Action non realisee" error (right lost meanwhile, or dace lock held).

## Scenario 3 — Point the callbacks at your own endpoint

```python
request.ajax_api = '@@my-ajax-api'      # before building the panel
```

`updateaction_viewurl`/`afterexecution_viewurl` honour it; your view then answers `op=update_action` (return one refreshed action body — `DaceUIAPIJson.update_action` shows how, including the virtual-start-action case rebuilt from `pd_id`/`action_id`/`behavior_id`) and `op=after_execution_action` (the unlock callback fired when a panel form is abandoned).

## Scenario 4 — The console screens

On a running site, as Admin: `<root>/runtime/@@Processes` lists the instances (a process without work-items shows as *blocked*), `@@StatisticRun` the dygraph dashboard; `<root>/process_definition_container/@@ProcessesDef` groups the definitions by discriminator; on a process, `@@Process` shows its definition's actions, `@@lesdonneesmanipulees` the entities of its execution context (current vs history), `@@actionsrealiser` the pending actions over the active involveds. Tables paginate through `page<tabid>`/`number<tabid>` query parameters (7 rows by default).

## Scenario 5 — Assign an activity or an action

On an `IActivity`: `@@assign_activity`; on an `IBusinessAction`: `@@assign_action` (current assignees + the Select2 form). Both run `set_assignment` through the `activity_pd` behaviours — assignment then feeds dace's `validate_action` pipeline (an assigned action only validates for its assignees).
