
import os
from apistar import Include
from apistar.handlers import docs_urls
from apistar.backends import django_orm
from apistar.frameworks.wsgi import WSGIApp as App

from core.routes import routes
from core.auth import BasicDjangoAuthentication


settings = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    'INSTALLED_APPS': ['core', 'django.contrib.auth', 'django.contrib.contenttypes', ],
    'AUTHENTICATION': [BasicDjangoAuthentication()],
}

if os.environ.get('TEST'):
    settings['DATABASES']['default']['NAME'] = 'test.db.sqlite3'

if os.environ.get('DEBUG'):
    routes.append(Include('/docs', docs_urls))

app = App(
    routes=routes,
    settings=settings,
    commands=django_orm.commands,
    components=django_orm.components,
)

if __name__ == '__main__':
    app.main()
