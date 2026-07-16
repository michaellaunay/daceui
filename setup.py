import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

requires = [
    'ecreall_dace',
    'ecreall_pontus',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_layout',
    'substanced',
    'waitress',
    ]

setup(name='ecreall_daceui',
      version='2.0.0.dev0',
      description='This the reusable ui parts for DaCE.',
      long_description=README + '\n\n' + CHANGES,
      long_description_content_type='text/markdown',
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.12",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        ],
      author='Amen Souissi',
      author_email='amensouissi@ecreall.com',
      maintainer='Michaël Launay (Logikascium)',
      url='https://github.com/michaellaunay/daceui/',
      project_urls={
          'Source': 'https://github.com/michaellaunay/daceui',
          'Tracker': 'https://github.com/michaellaunay/daceui/issues',
          'Historical upstream': 'https://github.com/ecreall/daceui',
      },
      keywords='pyramid ui workflow dace substanced',
      license="AGPLv3+",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="daceui",
      message_extractors={
          'daceui': [
              ('**.py', 'python', None), # babel extractor supports plurals
              ('**.pt', 'chameleon', None),
          ],
      },
      extras_require=dict(
          # 'pyramid_robot' (the historical robot layer) is unused by
          # the suite; the Phase 3 / M3 functional tests drive the app
          # over HTTP:
          test=['WebTest'],
      ),
      entry_points="""\
      [paste.app_factory]
      main = daceui:main
      """,
      )
