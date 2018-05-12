import django

SECRET_KEY = 'fake-key'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',

    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.table_block',
    'wagtail.contrib.forms',
    'wagtail.search',
    'wagtail.embeds',
    'wagtail.images',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.admin',
    'wagtail.core',

    'taggit',

    'wagtail_feeds',
    'tests',
)

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "wagtail"
    }
}

if django.VERSION >= (1, 10):
    MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'wagtail.core.middleware.SiteMiddleware',
    )
else:
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'wagtail.core.middleware.SiteMiddleware',
    )


ROOT_URLCONF = 'tests.urls'
WAGTAIL_SITE_NAME = "Test Site",
SITE_ID = 1
