from IBAS.settings.base import *
from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk

sentry_sdk.init(
    dsn="https://e0b7f7f1f8f04b39a633a223a86a8dca@o977207.ingest.sentry.io/5933669",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    #traces_sampler=traces_sampler,
    send_default_pii=True,
    environment="development",
)

ALLOW_HOST = ['*']  # 내부 개발자만 접근 가능!

WSGI_APPLICATION = 'IBAS.wsgi.dev.application'


