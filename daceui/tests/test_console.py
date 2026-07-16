# Copyright (c) 2026 by Logikascium under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Michaël Launay

"""daceui's first test suite (Phase 3 / M3).

Smoke-level but end to end: the self-hosting console definitions, the
``dace_ui_api`` utility, the action-panel rendering, the
``request.ajax_api`` override, the pagination helper and the HTTP
index page of the runtime.
"""
from daceui.testing import FunctionalTests
from daceui.interfaces import IDaceUIAPI

CONSOLE_PDS = {'runtime_pd', 'pdc_pd', 'pd_pd', 'p_pd', 'activity_pd'}


class TestDaceUIConsole(FunctionalTests):

    def _api(self):
        return self.registry.getUtility(IDaceUIAPI, 'dace_ui_api')

    def test_console_definitions_registered(self):
        """The five DaceManager definitions register at startup."""
        definitions = {d.id: d for d in self.def_container.definitions
                       if getattr(d, 'discriminator', None) == 'DaceManager'}
        self.assertEqual(set(definitions), CONSOLE_PDS)
        for definition in definitions.values():
            self.assertTrue(definition.isUnique)

    def test_dace_ui_api_utility(self):
        """The action-panel service is registered under 'dace_ui_api'."""
        from daceui.util import DaceUIAPI
        self.assertIsInstance(self._api(), DaceUIAPI)

    def test_calculatePage(self):
        """page<tabid>/number<tabid> pagination (7 per page by default)."""
        from daceui.util import calculatePage

        class DummyView(object):
            def __init__(self, values):
                self.values = values

            def params(self, name):
                return self.values.get(name)

        elements = list(range(20))
        page, pages, batch = calculatePage(
            elements, DummyView({}), 'tab')
        self.assertEqual((page, pages), (1, 3))
        self.assertEqual(batch, elements[:7])

        page, pages, batch = calculatePage(
            elements, DummyView({'pagetab': '3'}), 'tab')
        self.assertEqual((page, pages), (3, 3))
        self.assertEqual(batch, elements[14:])

    def test_update_actions_renders_panel(self):
        """The whole panel path: collect, render, assemble the entries."""
        runtime = self.app['runtime']
        api = self._api()
        all_actions = api.get_actions([runtime], self.request)
        self.assertTrue(all_actions)
        action_updated, messages, resources, actions = \
            api.update_actions(self.request, all_actions)
        self.assertFalse(action_updated)
        self.assertTrue(actions)
        for entry in actions:
            self.assertIn('body', entry)
            self.assertIn('action_id', entry)
            self.assertIn('actionurl_update', entry)

    def test_ajax_api_override(self):
        """``request.ajax_api`` re-points the panel callbacks (M4 hosts)."""
        runtime = self.app['runtime']
        api = self._api()
        self.request.ajax_api = '@@my-ajax-api'
        all_actions = api.get_actions([runtime], self.request)
        _, _, _, actions = api.update_actions(self.request, all_actions)
        self.assertTrue(actions)
        for entry in actions:
            self.assertIn('@@my-ajax-api', entry['actionurl_update'])

    def test_runtime_index_page(self):
        """HTTP end to end: SDI login, then the runtime index renders."""
        res = self.testapp.get('/manage')
        res.form['login'] = 'admin'
        res.form['password'] = 'admin'
        res = res.form.submit('form.submitted')
        self.assertEqual(res.status_int, 302)
        res = self.testapp.get('/runtime/@@index')
        self.assertEqual(res.status_int, 200)
        self.assertTrue(res.body)
