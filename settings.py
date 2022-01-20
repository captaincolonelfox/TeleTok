import os

API_TOKEN = os.environ.get('API_TOKEN')
SENTRY_DSN = os.getenv('SENTRY_DSN')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'Local')
USER_AGENT = os.getenv('USER_AGENT')
