"""
WSGI config for roche project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os


# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "roche.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roche.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
django_wsgi_application = get_wsgi_application()

def application(environ, start_response):
    # Get Docker link vars
    os.environ['DOCKER_PASSWORD'] = environ['DOCKER_PASSWORD']
    os.environ['DB_PORT_5432_TCP_ADDR'] = environ['DB_PORT_5432_TCP_ADDR']
    os.environ['DB_PORT_5432_TCP_PORT'] = environ['DB_PORT_5432_TCP_PORT']
    os.environ['XMLDB_PORT_8080_TCP_ADDR'] = environ['XMLDB_PORT_8080_TCP_ADDR']
    os.environ['XMLDB_PORT_8080_TCP_PORT'] = environ['XMLDB_PORT_8080_TCP_PORT']
    os.environ['SPARQL_PORT_3030_TCP_ADDR'] = environ['SPARQL_PORT_3030_TCP_ADDR']
    os.environ['SPARQL_PORT_3030_TCP_PORT'] = environ['SPARQL_PORT_3030_TCP_PORT']

    return django_wsgi_application(environ, start_response)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
