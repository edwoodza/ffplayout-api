import os

BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..', '..')))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dbs', 'player.sqlite3'),
    }
}
