# Copyright (c) 2026 by Logikascium under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Michaël Launay

"""Console views and JSON endpoint (T3).

Characterisation on the M3 harness. Pinned contracts:

- the five definition-side console views render (markers pinned —
  the ``panel-RuntimeStat`` template id, renamed 2026-07-17 from its
  historical typo);
- ``action_informations`` (renamed 2026-07-17; the typo alias is kept) has two faces, both pinned: on a FRESH app
  the console actions are oid-less and the START branch answers
  (``behavior_id + 'start_' + context_oid``, urls addressed by the
  ``(pd_id, action_id, behavior_id)`` triple); rendering a console
  view instantiates them, after which the OID branch composes
  ``behavior_id + action_oid + '_' + context_oid`` and addresses the
  urls by ``action_uid`` (default ``@@dace-ui-api-view`` endpoint);
- ``get_action_body`` answers a truthy layout ``Structure`` (and the
  ``include_resources`` variant adds the css/js dict);
- the JSON endpoint dispatches on ``op`` with an ASYMMETRIC error
  contract, pinned: the RESOLUTION paths are guarded (unknown or
  missing op and bogus uids answer ``{}``), but the RENDERING is not —
  a start action recomputed from a valid triple resolves, its view
  refuses, and pontus surfaces ``HTTPInternalServerError``; the
  ``action_uid`` path (post-instantiation) renders the body;
- ``statistic_dates`` buckets by minute and answers sorted pairs.
"""
import datetime

from substanced.util import get_oid

from daceui.testing import FunctionalTests
from daceui.interfaces import IDaceUIAPI


class Dummy(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


class TestConsoleViews(FunctionalTests):

    def _api(self):
        return self.registry.getUtility(IDaceUIAPI, 'dace_ui_api')

    def _first_action(self):
        runtime = self.app['runtime']
        context, action = self._api().get_actions(
            [runtime], self.request)[0]
        return context, action

    def test_console_views_render(self):
        from daceui import views
        runtime = self.app['runtime']
        container = self.app['process_definition_container']
        definition = sorted(container.definitions,
                            key=lambda d: d.__name__)[0]
        expectations = (
            (views.RuntimeView, runtime, 'processes_RuntimeView'),
            (views.ProcessDefinitionContainerView, container,
             'contenteditable'),
            (views.ProcessDefinitionView, definition,
             '<dt>Description</dt>'),
            # renamed 2026-07-17 from the historical typo
            (views.ProcessDefinitionStatisticView, definition,
             'panel-RuntimeStat'),
            (views.ProcessesPDDefinitionView, definition, 'alert'),
        )
        for view_class, context, marker in expectations:
            view = view_class(context, self.request)
            result = view.update()
            self.assertIn('coordinates', result, view_class.__name__)
            body = result['coordinates'][view.coordinates][0]['body']
            self.assertIn(marker, body, view_class.__name__)

    def test_action_informations_start_branch(self):
        # the historical typo stays importable
        from daceui.util import DaceUIAPI
        self.assertIs(DaceUIAPI.action_infomrations,
                      DaceUIAPI.action_informations)
        # fresh app: the console actions are oid-less — START branch
        context, action = self._first_action()
        infos = self._api().action_informations(
            action, context, request=self.request)
        self.assertEqual(
            sorted(infos),
            ['action', 'action_id', 'actionurl_after',
             'actionurl_update', 'view_title'])
        self.assertIs(infos['action'], action)
        context_oid = str(get_oid(context))
        self.assertEqual(infos['action_id'],
                         action.behavior_id + 'start_' + context_oid)
        for key, operation in (('actionurl_update', 'update_action'),
                               ('actionurl_after',
                                'after_execution_action')):
            url = infos[key]
            self.assertIn('@@dace-ui-api-view', url)
            self.assertIn('op=' + operation, url)
            self.assertIn('pd_id=' + action.node.process.id, url)
            self.assertIn('action_id=' + action.node.__name__, url)
            self.assertIn('behavior_id=' + action.behavior_id, url)
            self.assertIn('context_uid=' + context_oid, url)
            self.assertNotIn('action_uid=', url)

    def test_action_informations_oid_branch(self):
        # rendering a console view instantiates the actions
        from daceui import views
        runtime = self.app['runtime']
        views.RuntimeView(runtime, self.request).update()
        context, action = self._first_action()
        action_oid = str(get_oid(action))
        context_oid = str(get_oid(context))
        infos = self._api().action_informations(
            action, context, request=self.request)
        self.assertEqual(
            infos['action_id'],
            action.behavior_id + action_oid + '_' + context_oid)
        for key in ('actionurl_update', 'actionurl_after'):
            self.assertIn('action_uid=' + action_oid, infos[key])
            self.assertIn('context_uid=' + context_oid, infos[key])

    def test_get_action_body(self):
        context, action = self._first_action()
        body = self._api().get_action_body(context, self.request, action)
        self.assertTrue(len(body) > 0)
        body, resources = self._api().get_action_body(
            context, self.request, action, include_resources=True)
        self.assertEqual(sorted(resources), ['css_links', 'js_links'])
        self.assertTrue(len(body) > 0)

    def _json_call(self, context, params):
        from daceui.util import DaceUIAPIJson
        self.request.params = params
        return DaceUIAPIJson(context, self.request)()

    def test_json_endpoint_error_contract(self):
        context, _ = self._first_action()
        # never raises: {} on every error path
        self.assertEqual(self._json_call(context, {}), {})
        self.assertEqual(
            self._json_call(context, {'op': 'nonexistent'}), {})
        self.assertEqual(
            self._json_call(context, {'op': 'update_action',
                                      'action_uid': 'zzz'}), {})
        self.assertEqual(
            self._json_call(context, {'op': 'after_execution_action',
                                      'action_uid': 'zzz'}), {})

    def test_json_start_triple_resolves_then_render_refuses(self):
        """The asymmetric error contract, pinned: the triple RESOLVES
        (``_get_start_action`` recomputes through ``pd.start_process``
        on a fresh app), but the recomputed action's view refuses to
        render and pontus surfaces ``HTTPInternalServerError`` — the
        guarded ``{}`` contract covers resolution, not rendering.
        """
        from pyramid.httpexceptions import HTTPInternalServerError
        context, action = self._first_action()
        self.assertRaises(
            HTTPInternalServerError, self._json_call,
            context, {'op': 'update_action',
                      'pd_id': action.node.process.id,
                      'action_id': action.node.__name__,
                      'behavior_id': action.behavior_id})

    def test_json_update_action_by_uid(self):
        # instantiate first, then resolve by oid
        from daceui import views
        views.RuntimeView(self.app['runtime'], self.request).update()
        context, action = self._first_action()
        result = self._json_call(
            context, {'op': 'update_action',
                      'action_uid': str(get_oid(action)),
                      'context_uid': str(get_oid(context))})
        self.assertEqual(sorted(result), ['body'])
        self.assertTrue(len(str(result['body'])) > 0)

    def test_statistic_dates_buckets_by_minute(self):
        api = self._api()
        view = object()      # unused by the method
        self.assertEqual(api.statistic_dates(view, []), [])
        first = datetime.datetime(2016, 7, 14, 15, 30, 10)
        second = datetime.datetime(2016, 7, 14, 15, 30, 50)
        third = datetime.datetime(2016, 7, 14, 15, 31, 0)
        processes = [Dummy(created_at=first), Dummy(created_at=second),
                     Dummy(created_at=third)]
        self.assertEqual(
            api.statistic_dates(view, processes),
            [('2016-07-14 15:30:00', 2), ('2016-07-14 15:31:00', 1)])
