import os

API_TOKEN = os.environ.get('API_TOKEN')
SENTRY_DSN = os.getenv('SENTRY_DSN')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'Local')
USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0')
