"""
Django settings for IBAS project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from django.contrib.messages import constants as messages_constants
from pathlib import Path
import os
from my_root import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent.parent

ROOT_DIR = os.path.dirname(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG_MODE

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # 에디터 앱
    "django_summernote",
    # DB 관련 앱
    'DB',
    # 유저 관련 앱
    'member',
    # 메인 관련 앱
    'main',
    # 회계 관련 앱
    'bank',
    # 게시판 관련 앱
    'board',
    # 내 정보 관련 앱
    'my_info',
    # 회원 관리 관련 앱
    'staff',
    # 강의 관련 앱
    'lecture',
    # 덧글 관련 앱
    'comment',
    # widget_tweaks
    'widget_tweaks',
    # 템플릿에서 산술연산을 하기 위한 앱
    'mathfilters',
    # 소셜 로그인 패키지: allauth 관련
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # provider: 우선 구글
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.kakao',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'IBAS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            "templates",
            BASE_DIR / 'templates',
            MY_TEMPLATE_ROOT,
        ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.alarms',  # 알람 시스템을 위한 context_processor
                'utils.context_processors.chief',  # 하단바 회장 정보를 불러오기 위한 context_processor
                'utils.context_processors.login',  # 로그인을 위한 context_processor
                'utils.context_processors.login_check',  # 로그인 확인을 위한 context_processor
                'utils.context_processors.superuser_check',  # 슈퍼유저 확인을 위한 context_processor
                'utils.context_processors.is_active',
                'utils.context_processors.cfo_check',
                'utils.context_processors.get_policies',
            ],
        },
    },
]


#WSGI_APPLICATION = 'IBAS.wsgi.dev.application'
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = MY_DATABASE

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    MY_STATIC_ROOT
]
#STATICFILES_STORAGE = 'IBAS.storage.CompressAndHashStaticFilesStorage'  #'IBAS.storage.StaticFilesMd5HashingStorage'
# WHITENOISE_MANIFEST_STRICT = False  # 왜 안되지

# social 로그인 패키지 설정
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# 미디어 파일을 관리할 루트 media 디렉터리
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 각 media file에 대한 URL prefix
MEDIA_URL = '/media/'

# 소셜 로그인 관련 설정
SITE_ID = 2
LOGIN_REDIRECT_URL = '/user/pass'  # 로그인 성공시 리다이렉션 되는 URL 바꿀 필요가 있을 듯..
ACCOUNT_EMAIL_REQUIRED = True  # 이메일은 꼭 받게 만들기.
ACCOUNT_LOGOUT_ON_GET = True  # 로그 아웃 시 example.com사이트로 자동이동 하는 것 제거

# send email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ibasmail20@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# 브라우져 종료시 세션 만료
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MESSAGE_TAGS = {
    messages_constants.ERROR: 'danger'
}

# HTTPS
if IS_SERVER:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

X_FRAME_OPTIONS = 'SAMEORIGIN'

SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',
        'height': '480',
    }
}

SUMMERNOTE_THEME = 'bs3'
