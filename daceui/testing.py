# Copyright (c) 2026 by Logikascium under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Michaël Launay

"""Functional test harness (Phase 3 / M3 — daceui's first test suite).

Same shape as dace's and pontus's: a real Pyramid app (substanced +
dace + pontus + daceui) on a temporary file ZODB, request extensions
applied, admin logged in, a WebTest ``testapp`` for HTTP flows.
"""
import unittest

from pyramid.config import Configurator
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRequestExtensions
from pyramid import testing
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.threadlocal import get_current_request

from substanced.db import root_factory

from dace.util import get_userid_by_login
from dace.subscribers import stop_ioloop
from dace.testing import _TestingAuthenticationPolicy


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings, root_factory=root_factory)
    # pontus and daceui both declare a *default* layout; as sibling
    # includes they tie and pyramid raises a ConfigurationConflictError.
    # The application owns the tie-break (nova-ideo registers its own
    # layout); the harness plays the application:
    from daceui.layout import GlobalLayout
    config.add_layout(GlobalLayout, template='daceui:templates/master.pt')
    return config.make_wsgi_app()


def login(login):
    """Point the test authentication policy at the user of ``login``."""
    request = get_current_request()
    userid = get_userid_by_login(login, request)
    request.registry.registerUtility(
        _TestingAuthenticationPolicy(userid), IAuthenticationPolicy)


class FunctionalTests(unittest.TestCase):

    """Base class of the functional layers (see module docstring)."""

    def setUp(self):
        """Build the throwaway app and log in as admin."""
        import tempfile
        import os.path
        self.tmpdir = tempfile.mkdtemp()

        dbpath = os.path.join(self.tmpdir, 'test.db')
        uri = 'file://' + dbpath
        settings = {'zodbconn.uri': uri,
                    # pyramid_tm annotates the transaction with the user
                    # *before* traversal; substanced 1.0b1's groupfinder
                    # then reads request.context (see pontus, M2).
                    'tm.annotate_user': 'false',
                    'substanced.secret': 'sosecret',
                    'substanced.initial_login': 'admin',
                    'substanced.initial_password': 'admin',
                    'pyramid.includes': [
                        'substanced',
                        'pyramid_chameleon',
                        'pyramid_layout',
                        'pyramid_tm',
                        'dace',
                        'pontus',
                        'daceui',
                    ]}

        app = main({}, **settings)
        # substanced >= 1.0b1 registers request.mailer itself; override
        # with the dummy directly on the registry (see pontus, M2).
        from pyramid_mailer.testing import DummyMailer
        from pyramid_mailer.interfaces import IMailer
        app.registry.registerUtility(DummyMailer(), IMailer)

        self.db = app.registry._zodb_databases['']
        self.request = request = DummyRequest()
        self.request.test = True
        self.config = testing.setUp(registry=app.registry, request=request)

        extensions = app.registry.queryUtility(IRequestExtensions)
        if extensions is not None:
            from pyramid.request import apply_request_extensions
            apply_request_extensions(request, extensions=extensions)

        self.registry = self.config.registry
        self.app = root_factory(request)
        request.root = request.context = self.app
        self.users = self.app['principals']['users']
        login('admin')
        self.def_container = self.app['process_definition_container']

        from webtest import TestApp
        self.testapp = TestApp(app)
        import time
        time.sleep(2)

    def tearDown(self):
        """Stop the reactor, tear down, delete the temporary database."""
        stop_ioloop()
        import shutil
        testing.tearDown()
        self.db.close()
        shutil.rmtree(self.tmpdir)
