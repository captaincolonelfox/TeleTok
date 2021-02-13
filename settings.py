import os

API_TOKEN = os.environ.get('API_TOKEN')
SENTRY_DSN = os.getenv('SENTRY_DSN')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'Local')
DOWNLOAD_ERROR = os.getenv("DOWNLOAD_ERROR", "Error: Can't download video")