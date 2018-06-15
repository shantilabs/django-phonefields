USE_I18N = True
SECRET_KEY = '12345'

INSTALLED_APPS = (
    'test_app',
    'phonefields',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        #'NAME': 'test.sqlite3',
        'USER': '',
        'PASSWORD': '',
    }
}
