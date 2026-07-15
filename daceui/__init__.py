# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""daceui — the administration console of the dace engine, and the ajax
action-panel service the host applications consume. The console's own
screens are dace processes (see docs/en/architecture.md). ``main`` runs
daceui standalone; ``includeme`` wires it into a host application.
"""
from pyramid.config import Configurator
from pyramid.i18n import TranslationStringFactory

from substanced.db import root_factory


_ = TranslationStringFactory('daceui')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.add_translation_dirs('pontus:locale/')
    config.add_translation_dirs('dace:locale/')
    config.add_translation_dirs('deform:locale/')
    config.add_translation_dirs('colander:locale/')
    config.scan()
    config.add_static_view(
            'daceuistatic', 'daceui:static', cache_max_age=86400)
    return config.make_wsgi_app()


def include(config): # pragma: no cover
    """Inclusion split (historical): include the package."""
    config.include('.')


def scan(config): # pragma: no cover
    """Inclusion split (historical): scan the package."""
    config.scan('.')


def includeme(config): # pragma: no cover
    """Pyramid inclusion: scan the package and mount the static assets."""
    config.include(include)
    config.include(scan)
    config.add_static_view(
            'daceuistatic', 'daceui:static', cache_max_age=86400)
