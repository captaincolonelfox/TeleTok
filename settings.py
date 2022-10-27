import os

API_TOKEN = os.getenv('API_TOKEN')
USER_ID = os.getenv('USER_ID')
SENTRY_DSN = os.getenv('SENTRY_DSN')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'Local')
USER_AGENT = os.getenv('USER_AGENT')
