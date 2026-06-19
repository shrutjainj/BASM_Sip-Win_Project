"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import importlib

# Attempt to import Django's WSGI application factory. Use importlib so
# language servers that can't resolve Django from the current environment
# don't prevent the module from being parsed. If Django isn't available,
# provide a minimal WSGI app that returns an informative error.
try:
	get_wsgi_application = importlib.import_module('django.core.wsgi').get_wsgi_application
except Exception as e:  # pragma: no cover - fallback when Django isn't available
	def application(environ, start_response):
		start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
		msg = (
			'Django is not available or failed to import.\n'
			f'Import error: {e}\n'
			'Ensure Django is installed and PYTHONPATH/virtualenv is configured.'
		)
		return [msg.encode('utf-8')]
else:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
	application = get_wsgi_application()  # type: ignore[assignment]
