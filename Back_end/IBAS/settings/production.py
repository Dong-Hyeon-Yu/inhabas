from IBAS.settings.base import *
from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk

sentry_sdk.init(
    dsn="https://f51f9e76bd644fd3bb40b8c180ea4ac1@o1372531.ingest.sentry.io/6677587",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    #traces_sampler=traces_sampler,
    send_default_pii=True,
    environment="production",
)    


ADMINS = [
    ('Yejin', 'yyj11kr@naver.com'),
]

WSGI_APPLICATION = 'IBAS.wsgi.production.application'

# HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
