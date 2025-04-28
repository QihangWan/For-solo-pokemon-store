import os
from pathlib import Path
import dj_database_url  # 添加这一行以支持 PostgreSQL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-1234567890abcdef'

DEBUG = True

ALLOWED_HOSTS = ['*']

# 修改 CSRF_TRUSTED_ORIGINS，添加 HTTP 版本，确保匹配请求来源
CSRF_TRUSTED_ORIGINS = [
    'https://dialoginclude-tommylady-8000.codio-box.uk',
    'http://dialoginclude-tommylady-8000.codio-box.uk',  # 添加 HTTP 版本
]

# 禁用 CSRF_COOKIE_SECURE 和 SESSION_COOKIE_SECURE（开发环境）
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# 禁用缓存（开发环境）
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'naming',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pokemon_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pokemon_store.wsgi.application'

# 修改数据库配置，支持 SQLite（Codio）和 PostgreSQL（Heroku）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 如果有 DATABASE_URL 环境变量（Heroku 环境），使用 PostgreSQL
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(default=os.environ.get('DATABASE_URL'))

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "naming/static"]
STATIC_ROOT = BASE_DIR / 'staticfiles' 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
